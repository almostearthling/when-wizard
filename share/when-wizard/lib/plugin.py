# file: share/when-wizard/modules/plugin.py
# -*- coding: utf-8 -*-
#
# Base classes for When Wizard plugin containers
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import sys
import time
import json
import glob
import textwrap
import subprocess

from utility import load_icon, load_pixbuf, load_dialog, build_dialog
from utility import datastore, unique_str


class PluginConstants(object):
    PLUGIN_TYPE_TASK = 'task'
    PLUGIN_TYPE_CONDITION = 'condition'

    CATEGORY_TASK_APPS = 'apps'
    CATEGORY_TASK_SETTINGS = 'settings'
    CATEGORY_TASK_POWER = 'power'
    CATEGORY_TASK_SESSION = 'session'
    CATEGORY_TASK_FILEOPS = 'fileops'
    CATEGORY_TASK_MISC = 'misc'

    CATEGORY_COND_TIME = 'time'
    CATEGORY_COND_EVENT = 'event'
    CATEGORY_COND_MISC = 'misc'


PLUGIN_CONST = PluginConstants()


_PLUGIN_DESC_FORMAT_CONSOLE = """\
basename: {basename}
name: {name}
type: {plugin_type}
description: {description}
copyright: {author}, {copyright}
information: {help_string}"""

_PLUGIN_HELP_HEADER_LENGTH_CONSOLE = len(
    _PLUGIN_DESC_FORMAT_CONSOLE.split('\n')[-1]) - len('{help_string}')
_PLUGIN_HELP_LINE_LENGTH_CONSOLE = 78 - _PLUGIN_HELP_HEADER_LENGTH_CONSOLE
_PLUGIN_DESC_FORMAT_GUI = """\
{help_string}

({plugin_type}: {basename})\
"""
_PLUGIN_DESC_FORMAT_GUI_COPYRIGHT = """\n{copyright}, {author}"""

_PLUGIN_FILE_EXTENSIONS = ['.py']
_PLUGIN_UNIQUE_ID_MAGIC = '00wiz99_'
_PLUGIN_ASSOCIATION_ID_MAGIC = '00act99_'   # ACT = associate condittion + task


# all external task commands will be launched using a stub launcher
_WIZARD_LOADER = 'when-wizard'
_WIZARD_SUBCOMMAND = 'launcher'


# base for all plugins
class BasePlugin(object):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None):
        if self.__class__.__name__ == 'BasePlugin':
            raise TypeError("cannot instantiate abstract class")
        self.basename = basename
        self.module_basename = basename
        self.name = name
        self.description = description
        self.author = author
        self.copyright = copyright
        if icon is None:
            icon = 'puzzle'
        if help_string is None:
            help_string = description
        self.icon = icon
        self.help_string = ' '.join(help_string.split('\n'))
        self.category = None
        self.plugin_type = None
        self.stock = False
        self.module_path = None
        self.unique_id = _PLUGIN_UNIQUE_ID_MAGIC + '%s_%s' % (self.basename,
                                                              unique_str())

    @classmethod
    def factory(cls, d):
        plugin = cls(None, None, None, None, None)
        plugin.from_dict(d)
        return plugin

    # prepare for JSON
    def to_dict(self):
        return {
            'unique_id': self.unique_id,
            'basename': self.basename,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'copyright': self.copyright,
            'icon': self.icon,
            'help_string': self.help_string,
            'category': self.category,
            'plugin_type': self.plugin_type,
            'stock': self.stock,
            'module_basename': self.module_basename,
            'module_path': self.module_path,
            'plugin_class': self.__class__.__name__,
        }

    def from_dict(self, d):
        self.unique_id = d['unique_id']
        self.basename = d['basename']
        self.name = d['name']
        self.description = d['description']
        self.author = d['author']
        self.copyright = d['copyright']
        self.icon = d['icon']
        self.help_string = d['help_string']
        self.category = d['category']
        self.plugin_type = d['plugin_type']
        self.stock = d['stock']
        self.module_basename = d['module_basename']
        self.module_path = d['module_path']

    def to_itemdef_dict(self):
        return {}

    def to_itemdef(self):
        d = self.to_itemdef_dict()
        res = '[%s]\n' % self.unique_id
        for key in d:
            v = d[key]
            if v is not None:
                if isinstance(v, tuple):
                    sv = ', '.join(map(str, v))
                elif isinstance(v, list):
                    sv = '\n'
                    for x in v:
                        if isinstance(x, tuple):
                            s = ', '.join(map(str, x))
                        else:
                            s = str(x)
                        sv += '    %s' % s
                elif isinstance(v, dict):
                    sv = '\n'
                    for x in v:
                        sv += '    %s=%s\n' % (x, str(v[x]))
                else:
                    sv = str(v)
                res += '%s: %s\n' % (key, sv)
        res += '\n'
        return res

    # descriptive strings
    def desc_string_console(self):
        l_hs = textwrap.wrap(self.help_string,
                             width=_PLUGIN_HELP_LINE_LENGTH_CONSOLE)
        hs = ('\n' + _PLUGIN_HELP_HEADER_LENGTH_CONSOLE * ' ').join(l_hs)
        kw = self.to_dict()
        kw['help_string'] = hs
        s = _PLUGIN_DESC_FORMAT_CONSOLE.format(**kw)
        return s

    def desc_string_gui(self):
        s = _PLUGIN_DESC_FORMAT_GUI.format(**self.to_dict())
        if not self.stock:
            s += _PLUGIN_DESC_FORMAT_GUI_COPYRIGHT.format(**self.to_dict())
        return s

    # utility resource functions
    def get_dialog(self, name):
        return build_dialog(name, reverse_order=not self.stock)

    def get_image(self, name):
        return load_icon(name, reverse_order=not self.stock)

    # return the description of what/when will be done, or None if not set
    def summary_description(self):
        return None

    # virtual pane interface
    def get_pane(self):
        return None


# main abstract base classes
class TaskPlugin(BasePlugin):

    def __init__(self,
                 category,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None):
        if self.__class__.__name__ == 'TaskPlugin':
            raise TypeError("cannot instantiate abstract class")
        BasePlugin.__init__(self, basename, name, description,
                            author, copyright, icon, help_string)
        self.plugin_type = PLUGIN_CONST.PLUGIN_TYPE_TASK
        self.category = category
        self.command_line = None
        self.process_wait = False
        # TODO: add other task related data, such as outcome control and its
        #       modifiers (case sensitivity, RE, etc), environment variables

    @classmethod
    def factory(cls, d):
        plugin = cls(None, None, None, None, None, None)
        plugin.from_dict(self)
        return plugin

    def command(self):
        loader_path = os.path.join(APP_BIN_FOLDER, _WIZARD_LOADER)
        return '%s %s %s %s' % (loader_path, _WIZARD_SUBCOMMAND,
                                self.module_basename, self.unique_id)

    def to_dict(self):
        d = BasePlugin.to_dict(self)
        d['command_line'] = self.command_line
        d['process_wait'] = self.process_wait
        # TODO: add here common data from further specifications
        return d

    def to_itemdef_dict(self):
        d = BasePlugin.to_itemdef_dict(self)
        d['type'] = 'task'
        d['command'] = self.command()
        # TODO: add here common data from further specifications
        return d

    def from_dict(self, d):
        BasePlugin.from_dict(self, d)
        self.command_line = d['command_line']
        self.process_wait = d['process_wait']

    def run(self):
        new_session = not self.process_wait
        if self.command_line:
            subprocess.call(self.command_line,
                            start_new_session=new_session, shell=True)
            return True
        else:
            return False


class ConditionPlugin(BasePlugin):

    def __init__(self,
                 category,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None):
        if self.__class__.__name__ == 'ConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BasePlugin.__init__(self, basename, name, description,
                            author, copyright, icon, help_string)
        self.plugin_type = PLUGIN_CONST.PLUGIN_TYPE_CONDITION
        self.category = category
        self.task_list = []

    @classmethod
    def factory(cls, d):
        plugin = cls(None, None, None, None, None, None)
        plugin.from_dict(self)
        return plugin

    def to_itemdef_dict(self):
        d = BasePlugin.to_itemdef_dict(self)
        d['type'] = 'condition'
        d['task names'] = tuple(self.task_list)
        return d

    def to_dict(self):
        d = BasePlugin.to_dict(self)
        d['task_names'] = self.task_list
        return d

    def from_dict(self, d):
        ConditionPlugin.from_dict(self, d)
        self.task_list = d['task_names']

    def set_task(self, taskname):
        self.task_list = [taskname]

    def reset_tasks(self):
        self.task_list = []

    def add_task(self, taskname):
        self.task_list.append(taskname)

    def startup_check(self):
        return False


class TimeConditionPlugin(ConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None):
        ConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_TIME,
                                 basename, name, description, author,
                                 copyright, icon, help_string)
        self.timespec = {
            'year': None,
            'month': None,
            'day': None,
            'hour': None,
            'minute': None,
            'weekday': None,
        }

    @classmethod
    def factory(cls, d):
        plugin = cls(None, None, None, None, None)
        plugin.from_dict(self)
        return plugin

    def to_dict(self):
        d = ConditionPlugin.to_dict(self)
        d['timespec'] = self.timespec
        return d

    def from_dict(self, d):
        ConditionPlugin.from_dict(self, d)
        self.timespec = d['timespec']

    def to_itemdef_dict(self):
        d = ConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'time'
        for k in self.timespec:
            d[k] = self.timespec[k]
        return d


# function to load a plugin as a module
def load_plugin_module(basename, stock=False):
    base = APP_PLUGIN_FOLDER if stock else USER_PLUGIN_FOLDER
    for ext in _PLUGIN_FILE_EXTENSIONS:
        basename_ext = basename + ext
        path = os.path.join(base, basename_ext)
        if os.path.exists(path):
            break
        else:
            path = None
    if path:
        from importlib.machinery import SourceFileLoader
        module = SourceFileLoader(basename, path).load_module()
        return module
    else:
        return None


# plugin data and registration management
def add_to_file(plugin, f):
    f.write(plugin.to_itemdef())
    return True


def direct_register(plugin):
    # TODO: write DBus code to directly register the plugin
    return False


def store_plugin(plugin):
    datastore.put(plugin.unique_id, json.dumps(plugin.to_dict()))
    return plugin.unique_id


def store_association(cond_plugin, *task_plugins):
    if len(task_plugins) < 1:
        raise ValueError("expected at least one task plugin")
    l = []
    if not isinstance(cond_plugin, ConditionPlugin):
        raise TypeError("expected a ConditionPlugin")
    else:
        l.append(cond_plugin.unique_id)
    for p in task_plugins:
        if not isinstance(p, TaskPlugin):
            raise TypeError("expected a TaskPlugin")
        else:
            l.append(p.unique_id)
    association_id = _PLUGIN_ASSOCIATION_ID_MAGIC + unique_str()
    datastore.put(association_id, json.dumps(l))
    return association_id


def retrieve_plugin(plugin, unique_id):
    d = json.loads(datastore.get(unique_id))
    # class_ = {
    #     'TaskPlugin': TaskPlugin,
    #     'TimeConditionPlugin': TimeConditionPlugin,
    #     # TODO: add remaining concrete plugin types here
    # }[d['plugin_class']]
    plugin.from_dict(d)
    return plugin


def retrieve_association(association_id):
    return json.loads(datastore.get(association_id))


def retrieve_plugin_ids():
    l = []
    for unique_id in datastore:
        if unique_id.startswith(_PLUGIN_UNIQUE_ID_MAGIC):
            l.append(unique_id)
    return l


def retrieve_association_ids():
    l = []
    for unique_id in datastore:
        if unique_id.startswith(_PLUGIN_ASSOCIATION_ID_MAGIC):
            l.append(unique_id)
    return l


# find plugins dynamically
def _plugins_names(basedir):
    r = []
    for x in _PLUGIN_FILE_EXTENSIONS:
        li = glob.glob(os.path.join(basedir, '*' + x))
        for y in li:
            r.append(os.path.basename(y)[:-len(x)])
    return r


def stock_plugins_names():
    return _plugins_names(APP_PLUGIN_FOLDER)


def user_plugins_names():
    return _plugins_names(USER_PLUGIN_FOLDER)


# end.
