# file: share/when-wizard/modules/plugin.py
# -*- coding: utf-8 -*-
#
# Base classes for When Wizard plugin containers
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import sys
import json
import textwrap
import subprocess


class PluginConstants(object):
    PLUGIN_TYPE_TASK = 'task'
    PLUGIN_TYPE_CONDITION = 'condition'

    CATEGORY_TASK_APPS = 'apps'
    CATEGORY_TASK_SETTINGS = 'settings'
    CATEGORY_TASK_POWER = 'power'
    CATEGORY_TASK_FILEOPS = 'fileops'

    CATEGORY_COND_TIME = 'time'
    CATEGORY_COND_INTERVAL = 'interval'
    CATEGORY_COND_EVENT = 'event'
    CATEGORY_COND_MISC = 'misc'


CONST = PluginConstants()


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

_PLUGIN_UNIQUE_ID_INDEX = 1


class BasePlugin(object):

    def __init__(self,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 help_string=None):
        global _PLUGIN_UNIQUE_ID_INDEX
        if self.__class__.__name__ == 'BasePlugin':
            raise TypeError("cannot instantiate abstract class")
        self.basename = basename
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
        self.module_basename = None
        self.module_path = None
        self.unique_id = '%s_%s' % (
            self.basename, ('000000' + str(_PLUGIN_UNIQUE_ID_INDEX))[-6:])
        _PLUGIN_UNIQUE_ID_INDEX += 1

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
            res += '%s: %s' % (key, sv)
        res += '\n'
        return res

    def register(self):
        filename = os.tmpnam()
        with open(filename, 'w') as f:
            f.write(self.to_itemdef())
        return subprocess.call(['when-command', '--item-add', filename])

    def unregister(self):
        return subprocess.call(['when-command', '--item-del', self.unique_id])

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
        # if self.__class__.__name__ == 'TaskPlugin':
        #     raise TypeError("cannot instantiate abstract class")
        BasePlugin.__init__(self, basename, name, description,
                            author, copyright, icon, help_string)
        self.plugin_type = CONST.PLUGIN_TYPE_TASK
        self.category = category

    def to_itemdef_dict(self):
        d = BasePlugin.to_itemdef_dict()
        d['type'] = 'task'
        return d

    def run(self):
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
        # if self.__class__.__name__ == 'ConditionPlugin':
        #     raise TypeError("cannot instantiate abstract class")
        BasePlugin.__init__(self, basename, name, description,
                            author, copyright, icon, help_string)
        self.plugin_type = CONST.PLUGIN_TYPE_CONDITION
        self.category = category

    def to_itemdef_dict(self):
        d = BasePlugin.to_itemdef_dict()
        d['type'] = 'condition'
        return d

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
        ConditionPlugin.__init__(self, CONST.CATEGORY_COND_TIME, basename,
                                 name, description, author, copyright,
                                 icon, help_string)
        self.time_spec = None


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


# end.
