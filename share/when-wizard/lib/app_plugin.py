# file: share/when-wizard/modules/wizard.py
# -*- coding: utf-8 -*-
#
# Base class for a When Wizard plugin container
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import textwrap


_PLUGIN_DESC_FORMAT = """\
basename: %s,
name: %s
type: %s
description: %s
copyright: %s, %s
information: %s"""
_PLUGIN_HELP_HEADER_LENGTH = len(_PLUGIN_DESC_FORMAT.split('\n')[-1]) - 2
_PLUGIN_HELP_LINE_LENGTH = 78 - _PLUGIN_HELP_HEADER_LENGTH


class ApplicationPluginConstants(object):
    PLUGIN_TYPE_TASK = 'task'
    PLUGIN_TYPE_CONDITION = 'condition'


APPLICATION_PLUGIN_CONSTANTS = ApplicationPluginConstants()


class ApplicationPlugin(object):

    def __init__(self,
                 plugintype,
                 category,
                 basename,
                 name,
                 description,
                 author,
                 copyright,
                 icon=None,
                 helpstring=None,
                 default=False,
                 ):
        self.plugintype = plugintype
        self.category = category
        self.basename = basename
        self.name = name
        self.description = description
        self.author = author
        self.copyright = copyright
        if icon is None:
            icon = 'puzzle'
        if helpstring is None:
            helpstring = description
        self.icon = icon
        self.helpstring = helpstring
        self.default = default
        self.module = None

    def desc_string(self):
        l_hs = textwrap.wrap(self.helpstring, width=_PLUGIN_HELP_LINE_LENGTH)
        hs = ('\n' + _PLUGIN_HELP_HEADER_LENGTH * ' ').join(l_hs)
        s = _PLUGIN_DESC_FORMAT % (
            self.basename,
            self.name,
            self.plugintype,
            self.description,
            self.copyright,
            self.author,
            hs,
        )
        return s


# end.
