# file: share/when-wizard/lib/itemimport.py
# -*- coding: utf-8 -*-
#
# Handle items imported from Item Definition Files
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


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


# end.
