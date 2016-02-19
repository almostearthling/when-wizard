# file: share/when-wizard/templates/template-cond-command-plugin.py
# -*- coding: utf-8 -*-
#
# Template for a command based condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import locale
from plugin import CommandConditionPlugin, PLUGIN_CONST, plugin_name

# Gtk might be needed: uncomment if this is the case
# from gi.repository import Gtk


# setup localization for both plugin text and configuration pane
# locale.setlocale(locale.LC_ALL, locale.getlocale())
# locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
# locale.textdomain(APP_NAME)
# _ = locale.gettext

# if localization is supported, uncomment the lines above configure
# them as appropriate, and remove this replacement function
def _(x):
    return x


HELP = _("""\
This is a template for a generic command condition plugin: it can be expanded
suitably to the needs of the plugin. A command line based condition plugin
must provide the full command line to be executed for the condition to be
verified: if the command is successful (zero-status) the condition is true.
""")


# class for a plugin: the derived class name should always be Plugin
class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Template"),
            description=_("Explain here what it does"),
            author="John Smith",
            copyright="Copyright (c) 2016",
            icon='puzzle',
            help_string=HELP,
            version="0.1.0",
        )
        # to repeat checks after first success uncomment the following line
        # self.repeat = True

        # the icon resource is only needed if the plugin uses a custom icon
        # self.graphics.append('plugin_icon.png')

        # the items below might be not needed and can be deleted if the
        # plugin does not have a configuration panel
        self.resources.append('plugin_template.glade')
        self.builder = self.get_dialog('plugin_template')
        self.plugin_panel = None
        self.forward_allowed = False        # forward not enabled by default

        # define this only if the plugin provides one or more scripts
        # self.scripts.append('needed_script.sh')

        # mandatory or anyway structural variables and object values follow:
        self.command_line = None            # full command line to run
        self.summary_description = None     # must be set for all plugins

        # this variable is defined here only for demonstrational purposes
        self.value = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    # all following methods are optional

    def click_btnDo(self, obj):
        o = self.builder.get_object
        o('txtEntry').set_text("Some text")

    def change_entry(self, obj):
        o = self.builder.get_object
        self.value = o('txtEntry').get_text()
        if self.value:
            self.summary_description = _(
                "Something will be done with %s") % self.value
            self.allow_forward(True)
        else:
            self.summary_description = None
            self.allow_forward(False)


# end.
