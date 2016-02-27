# file: share/when-wizard/lib/itemimport.py
# -*- coding: utf-8 -*-
#
# Handle items imported from Item Definition Files
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import re
import dbus
import json
import configparser
from utility import datastore, unique_str, when_proxy


_IDF_UNIQUE_ID_MAGIC = '00wiz99*'


# partially parse a string containing an IDF and retrieve items and types
def idf_items(s):
    parser = configparser.ConfigParser()
    try:
        parser.read_string(s)
        items = []
        for item in parser.sections():
            item_type = parser.get(item, 'type').lower()
            if item_type == 'task':
                prefix = 'tasks'
            elif item_type == 'condition':
                prefix = 'conditions'
            elif item_type == 'signal_handler':
                prefix = 'sighandlers'
            else:
                return None
            items.append(prefix + ':' + item)
        return items
    except configparser.Error:
        return None


# this module contains some more trickery to check whether or not an IDF can
# be imported into the When Wizard environment: the code will be a little
# more complicated, but this allows to avoid exceptions as a way to report
# failures to the calling application

def idf_exists(name):
    unique_id = _IDF_UNIQUE_ID_MAGIC + name
    if unique_id in datastore:
        return True
    return False


def idf_installed_list():
    elems = []
    for elem in datastore:
        if elem.startswith(_IDF_UNIQUE_ID_MAGIC):
            name = elem[len(_IDF_UNIQUE_ID_MAGIC):]
            elems.append(name)
    return elems


def idf_installed_items(name):
    if not idf_exists(name):
        return None
    unique_id = _IDF_UNIQUE_ID_MAGIC + name
    return json.loads(datastore.get(unique_id))


def idf_install(name, s, force=True):
    if idf_exists(name):
        return False
    unique_id = _IDF_UNIQUE_ID_MAGIC + name
    proxy = when_proxy()
    if proxy is None:
        return False
    items = idf_items(s)
    if items is None:
        return False
    if not proxy.AddItemsBatch(s):
        return False
    datastore.put(unique_id, json.dumps(items))
    return True


# when it fails it returns zero or less
def idf_remove(name):
    if not idf_exists(name):
        return 0
    proxy = when_proxy()
    if proxy is None:
        return 0
    items = idf_installed_items(name)
    conditions = [x for x in items if x.startswith('conditions' + ':')]
    tasks = [x for x in items if x.startswith('tasks' + ':')]
    sighandlers = [x for x in items if x.startswith('sighandlers' + ':')]
    error = 0
    for item in conditions:
        if not proxy.RemoveItem(item):
            error += 1
    for item in tasks:
        if not proxy.RemoveItem(item):
            error += 1
    for item in sighandlers:
        if not proxy.RemoveItem(item):
            error += 1
    unique_id = _IDF_UNIQUE_ID_MAGIC + name
    if not error:
        datastore.remove(unique_id)
        return 1
    else:
        return -error


##############################################################################
# Parametrized IDF handling
#
# Parametrized IDFs can reference user-modifiable parameters, which have to
# be defined in the file itself; when a IDF file is loaded, the manager
# interface shows a dialog box containing fields, one for each parameter,
# preset to their default values: the user can either modify the values or
# accept the defaults. Parameters start with an at-sign ('@') both in their
# definition line and when referenced: definition lines start with the
# parameter identifier followed by attributes that help the UI build a
# suitable configuration dialog.
#
# Possible definition lines are:
# @param_id desc:s[tring]:default[:regex]
# @param_id desc:i[nteger]:default[:min:max]
# @param_id desc:r[eal]:default[:min:max]
# @param_id desc:c[hoice]:default:value1,value2,...,valueN
# @param_id desc:f[ile]:default
# @param_id desc:d[irectory]:default
#
# where default is the default value (it can be the empty string); the choice
# case can be used to create combo boxes with fixed values to choose from;
# the type prefixes can be partial or even just one letter, for strings a
# regular expression can (and should) be provided to check for validity and
# for numerics minimum and maximum values can be provided too. Note that for
# choices, if default is not in value1, ..., valueN it will just be added.
#
# Parameter substitution is performed string-wise in the file: if correctness
# verifiers are not provided, the result might break the IDF making it invalid
# and When will refuse to import it. Of course in such case the user will be
# notified of the import failure by a message box.
#
# WARNING: incorrect param lines are skipped as param lines and sent back to
#          the file as they are!
#
# TODO: this comment MUST GO AWAY and its contents find a way into the docs.

VALIDATE_PARAM_NAME = re.compile(r"^\@[a-zA-Z][a-zA-Z0-9_]*$")


# here I carefully avoid to have to write a parser for a small language like
# this: the only thing I care about is to have the chance to put semicolons
# and commas in string defaults and choice values
def param_file(s):
    out_lines = []
    params = {}
    for line in s.split('\n'):
        clean_line = line.strip()
        if not clean_line.startswith('@'):
            out_lines.append(line)
        else:
            control = lambda x: True
            choices = None
            try:
                param, rest = clean_line.split(maxsplit=1)
                if not VALIDATE_PARAM_NAME.match(param):
                    raise ValueError
                description, rest = rest.split(':', maxsplit=1)
                t, rest = rest.split(':', maxsplit=1)
                t = t.lower()
                if 'string'.startswith(t):
                    param_type = 'string'
                    default = ''
                    while rest and rest[0] != ':':
                        if rest[0] == '\\':
                            rest = rest[1:]
                        default += rest[0]
                        rest = rest[1:]
                    rest = rest[1:]
                    if rest:
                        try:
                            control = re.compile(rest).match
                        except:
                            raise ValueError
                elif 'integer'.startswith(t):
                    param_type = 'integer'
                    if ':' in rest:
                        default, smin, smax = [int(x) for x in rest.split(':')]
                        control = lambda x: smin <= x <= smax
                    else:
                        default = int(rest)
                elif 'real'.startswith(t):
                    param_type = 'real'
                    if ':' in rest:
                        default, smin, smax = [
                            float(x) for x in rest.split(':')]
                        control = lambda x: smin <= x <= smax
                    else:
                        default = float(rest)
                elif 'choice'.startswith(t):
                    param_type = 'choice'
                    default, rest = rest.split(':', 1)
                    choices = []
                    buf = ''
                    while rest:
                        if rest[0] == ',':
                            if buf not in choices:
                                choices.append(buf)
                            buf = ''
                            rest = rest[1:]
                        else:
                            if rest[0] == '\\':
                                rest = rest[1:]
                            buf += rest[0]
                            rest = rest[1:]
                    if default not in choices:
                        choices.insert(0, default)
                elif 'file'.startswith(t):
                    param_type = 'file'
                    default = rest
                elif 'directory'.startswith(t):
                    param_type = 'directory'
                    default = rest
                else:
                    raise ValueError
                params[param] = (
                    param_type, description, default, control, choices)
            except (TypeError, ValueError) as e:
                out_lines.append(clean_line)
                continue
    return '\n'.join(out_lines), params


# this avoids to have to deal with regex group substitutions where just fixed
# strings have to be replaced: the point in splitting the line in pieces and
# looking ahead in the first character of the next piece is that we do not
# want to replace a parameter that can be the substring of another one with
# that other one; the other possible strategy is to sort parameter names in
# descending order and replace them abruptly in the entire string: in this
# way we are sure that parameter names that contain other parameter names are
# processed before the shorter ones and thus remove the chance of overlapping
def replace_param(s, param, value):
    out_lines = []
    s_value = str(value)
    for line in s.split('\n'):
        clean_line = line.strip()
        if clean_line.startswith('#') or clean_line.startswith(';'):
            out_lines.append(line)
        else:
            s = ''
            pieces = line.split(param)
            while pieces:
                s += pieces[0]
                pieces = pieces[1:]
                if pieces:
                    if pieces[0] and (
                       pieces[0][0].isalnum() or pieces[0][0] == '_'):
                        s += param
                    else:
                        s += value
                else:
                    s += value
            out_lines.append(s)
    return '\n'.join(out_lines)


# as said above both options are possible: let's keep the formally correct
# one for now, for a try: it can be changed easily to the commented out one
def replace_params(s, param_dict):
    params = param_dict.keys()
    params.sort(reverse=True)
    for x in params:
        # s = s.replace(x, param_dict[x])
        s = replace_param(s, x, param_dict[x])
    return s


# end.
