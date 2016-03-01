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
from collections import OrderedDict
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


# Parametrized IDF handling
VALIDATE_PARAM_NAME = re.compile(r"^\@[a-zA-Z][a-zA-Z0-9_]*$")


# here I carefully avoid to have to write a parser for a small language like
# this: the only thing I care about is to have the chance to put semicolons
# and commas in string defaults and choice values
def param_file(s):

    def try_conversion(num, t):
        try:
            y = t(num)
            return True
        except:
            return False

    out_lines = []
    params = OrderedDict()
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
                        control = lambda x: smin <= int(x) <= smax
                    else:
                        default = int(rest)
                        control = lambda x: try_conversion(x, int)
                elif 'real'.startswith(t):
                    param_type = 'real'
                    if ':' in rest:
                        default, smin, smax = [
                            float(x) for x in rest.split(':')]
                        control = lambda x: smin <= float(x) <= smax
                    else:
                        default = float(rest)
                        control = lambda x: try_conversion(x, float)
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
                    if buf and buf not in choices:
                        choices.append(buf)
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
# strings have to be replaced. The strategy is to sort parameter names in
# descending order and replace them abruptly in the entire string: in this
# way we are sure that parameter names that contain other parameter names are
# processed before the shorter ones and thus remove the chance of overlapping
def replace_params(s, param_dict):
    params = list(param_dict.keys())
    params.sort(reverse=True)
    for x in params:
        s = s.replace(x, str(param_dict[x]))
    return s


# end.
