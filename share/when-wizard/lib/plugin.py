# file: share/when-wizard/modules/plugin.py
# -*- coding: utf-8 -*-
#
# Base classes for When Wizard plugin containers
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import json
import textwrap


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

    # prepare for JSON
    def to_dict(self):
        return {
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

    def register(self):
        raise TypeError("this item cannot be registered")

    def run(self):
        return True


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

    def register(self):
        raise TypeError("this item cannot be registered")

    def startup_check(self):
        return False


# end.
