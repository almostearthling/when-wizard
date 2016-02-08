# file: share/when-wizard/lib/plugin.py
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

##############################################################################
# plugin related inner constants


# public constants, to import: 'from plugin import ConcretePlugin, PLUGIN_CONST'
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


# private internals
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


##############################################################################
# base for all plugins
class BasePlugin(object):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'BasePlugin':
            raise TypeError("cannot instantiate abstract class")
        self.version = version
        self.basename = basename
        self.unique_id = _PLUGIN_UNIQUE_ID_MAGIC + '%s_%s' % (
            self.basename, unique_str())
        self.module_basename = basename
        self.name = name
        self.description = description
        self.author = author
        self.copyright = copyright
        if icon is None:
            icon = 'puzzle'
        if help_string is None:
            help_string = description
        self.summary_description = self.description
        self.icon = icon
        self.help_string = ' '.join(help_string.split('\n'))
        self.category = None
        self.plugin_type = None
        self.stock = False
        self.module_path = None
        self.forward_allowed = True
        self._forward_button = None

    # prepare for JSON
    def to_dict(self):
        return {
            'unique_id': self.unique_id,
            'basename': self.basename,
            'name': self.name,
            'version': self.version,
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
        self.version = d['version']
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

    def to_item_dict(self):
        return {}

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

    # plugin level persistent data
    def data_store(self, data_dic):
        if self.stock:
            key = 's:%s' % self.basename
        else:
            key = 'u:%s' % self.basename
        datastore.put(json.dumps(key, data_dic))

    def data_retrieve(self):
        if self.stock:
            key = 's:%s' % self.basename
        else:
            key = 'u:%s' % self.basename
        return json.loads(datastore.get(key))

    # configuration retrieval utility
    # def get_config(self, section, entry, default=None):
    #     return USER_CONFIG.get(section, entry, default)

    # retrieve a script in the correct folder and return its full path
    def get_script(self, filename):
        if self.stock:
            folder = os.path.join(APP_DATA_FOLDER, 'scripts')
        else:
            folder = USER_SCRIPT_FOLDER
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            return path
        else:
            return None

    # virtual pane interface
    def get_pane(self):
        return None

    def set_forward_button(self, btn=None):
        self._forward_button = btn

    def allow_forward(self, allow=True):
        if self._forward_button is not None:
            self._forward_button.set_sensitive(allow)


##############################################################################
# the following are all abstract base classes: real plugins have to derive
# from these, and in turn expose a constructor that requires no arguments,
# of course except self: this allows the other parts of the program to
# instantiate real plugins whenever it's needed and initialize them on the
# fly upon retrieval (via, for instance, from_dict and retrieve_plugin)

class TaskPlugin(BasePlugin):

    def __init__(self,
                 category,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
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

    def to_dict(self):
        d = BasePlugin.to_dict(self)
        d['command_line'] = self.command_line
        d['process_wait'] = self.process_wait
        # TODO: add here common data from further specifications
        return d

    def from_dict(self, d):
        BasePlugin.from_dict(self, d)
        self.command_line = d['command_line']
        self.process_wait = d['process_wait']

    def to_item_dict(self):
        d = BasePlugin.to_item_dict(self)
        d['type'] = 'task'
        d['task_id'] = 1
        d['task_name'] = self.unique_id
        d['environment_vars'] = []
        d['include_env'] = True
        d['success_stdout'] = None
        d['success_stderr'] = None
        d['success_status'] = 0
        d['failure_stdout'] = None
        d['failure_stderr'] = None
        d['failure_status'] = None
        d['match_exact'] = False
        d['case_sensitive'] = False
        d['command'] = self.command()
        d['startup_dir'] = None
        d['match_regexp'] = False
        return d

    def to_itemdef_dict(self):
        d = BasePlugin.to_itemdef_dict(self)
        d['type'] = 'task'
        d['command'] = self.command()
        # TODO: add here common data from further specifications
        return d

    def command(self):
        loader_path = os.path.join(APP_BIN_FOLDER, _WIZARD_LOADER)
        return '%s %s %s %s' % (loader_path, _WIZARD_SUBCOMMAND,
                                self.module_basename, self.unique_id)

    def run(self):
        new_session = not self.process_wait
        if self.command_line:
            subprocess.call(self.command_line,
                            start_new_session=new_session, shell=True)
            return True
        else:
            return False


# this class is not meant to be directly derived from (thus Base... prefix)
class BaseConditionPlugin(BasePlugin):

    def __init__(self,
                 category,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'ConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BasePlugin.__init__(self, basename, name, description,
                            author, copyright, icon, help_string)
        self.plugin_type = PLUGIN_CONST.PLUGIN_TYPE_CONDITION
        self.category = category
        self.task_list = []

    def to_dict(self):
        d = BasePlugin.to_dict(self)
        d['task_names'] = self.task_list
        return d

    def from_dict(self, d):
        ConditionPlugin.from_dict(self, d)
        self.task_list = d['task_names']

    def to_item_dict(self):
        d = BasePlugin.to_item_dict(self)
        d['type'] = 'condition'
        d['subtype'] = None
        d['cond_id'] = 1
        d['cond_name'] = self.unique_id
        d['type'] = 'condition'
        d['task_names'] = self.task_list
        d['repeat'] = True
        d['exec_sequence'] = True
        d['suspended'] = False
        d['break_failure'] = False
        d['break_success'] = False
        return d

    def to_itemdef_dict(self):
        d = BasePlugin.to_itemdef_dict(self)
        d['type'] = 'condition'
        d['task names'] = tuple(self.task_list)
        return d

    def set_task(self, taskname):
        self.task_list = [taskname]

    def reset_tasks(self):
        self.task_list = []

    def add_task(self, taskname):
        self.task_list.append(taskname)

    def startup_check(self):
        return False


# NOTE: the following are the actual base classes to derive from
class IntervalConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'IntervalConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_TIME,
                                     basename, name, description, author,
                                     copyright, icon, help_string)
        self.interval = 0

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['interval'] = self.interval
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.interval = d['interval']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'interval'
        d['interval minutes'] = self.interval
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'IntervalBasedCondition'
        d['interval'] = self.interval * 60
        return d


class TimeConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'TimeConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_TIME,
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

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['timespec'] = self.timespec
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.timespec = d['timespec']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'time'
        for k in self.timespec:
            if k != 'weekday' or self.timespec[k] is None:
                d[k] = self.timespec[k]
            else:
                d[k] = [
                    'monday',
                    'tuesday',
                    'wednesday',
                    'thursday',
                    'friday',
                    'saturday',
                    'sunday',
                ][self.timespec[k]]
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'TimeBasedCondition'
        for k in self.timespec:
            d[k] = self.timespec[k]
        return d


class IdleConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'IdleConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_TIME,
                                     basename, name, description, author,
                                     copyright, icon, help_string)
        self.idlemins = 0

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['idlemins'] = self.idlemins
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.idlemins = d['idlemins']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'idle_session'
        d['idle minutes'] = self.idlemins
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'IdleTimeBasedCondition'
        d['idle_secs'] = self.idlemins * 60
        return d


class CommandConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'CommandConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_MISC,
                                     basename, name, description, author,
                                     copyright, icon, help_string)
        self.command_line = None

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['command_line'] = self.command_line
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.command_line = d['command_line']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'command'
        d['command'] = self.command_line
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'CommandBasedCondition'
        d['match_exact'] = False
        d['match_regexp'] = False
        d['case_sensitive'] = False
        d['command'] = self.command_line
        d['expected_status'] = 0
        d['expected_stdout'] = None
        d['expected_stderr'] = None
        return d


class EventConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'EventConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_EVENT,
                                     basename, name, description, author,
                                     copyright, icon, help_string)
        self.event = None

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['event'] = self.event
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.event = d['event']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'event'
        d['event type'] = self.event
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'EventBasedCondition'
        d['event'] = self.event
        d['no_skip'] = False
        return d


class UserEventConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'UserEventConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_EVENT,
                                     basename, name, description, author,
                                     copyright, icon, help_string)
        self.event_name = None

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['event_name'] = self.event_name
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.event_name = d['event_name']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'user_event'
        d['event name'] = self.event_name
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'EventBasedCondition'
        d['event'] = 'dbus_signal:%s' % self.event_name
        d['no_skip'] = False
        return d


class FileChangeConditionPlugin(BaseConditionPlugin):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None,
                 version=None):
        if self.__class__.__name__ == 'FileChangeConditionPlugin':
            raise TypeError("cannot instantiate abstract class")
        BaseConditionPlugin.__init__(self, PLUGIN_CONST.CATEGORY_COND_EVENT,
                                     basename, name, description, author,
                                     copyright, icon, help_string)
        self.watched_path = None

    def to_dict(self):
        d = BaseConditionPlugin.to_dict(self)
        d['watched_path'] = self.watched_path
        return d

    def from_dict(self, d):
        BaseConditionPlugin.from_dict(self, d)
        self.event = d['watched_path']

    def to_itemdef_dict(self):
        d = BaseConditionPlugin.to_itemdef_dict(self)
        d['based on'] = 'file_change'
        d['watched path'] = self.watched_path
        return d

    def to_item_dict(self):
        d = BaseConditionPlugin.to_item_dict(self)
        d['subtype'] = 'PathNotifyBasedCondition'
        d['watched_paths'] = [self.watched_path]
        d['no_skip'] = False
        return d


##############################################################################
# utility functions: these can be used to manage plugin instances (the ones
# that have been created through concrete plugin classes) and for storage
# and retrieval; kept here because the scope is plugin related anyway

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


def store_plugin(plugin):
    datastore.put(plugin.unique_id, json.dumps(plugin.to_dict()))
    return plugin.unique_id


def store_association(cond_plugin, *task_plugins):
    if len(task_plugins) < 1:
        raise ValueError("expected at least one task plugin")
    l = []
    if not isinstance(cond_plugin, BaseConditionPlugin):
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


# this expects that the provided plugin reference is of the correct type
# it returns the plugin object for symmetry with the association based one
def retrieve_plugin(plugin, unique_id):
    d = json.loads(datastore.get(unique_id))
    if plugin.__class__.__name__ != d['plugin_class']:
        raise ValueError("plugin of class %s expected" % d['plugin_class'])
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
