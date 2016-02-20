# file: share/when-wizard/templates/cond-misc-command.py
# -*- coding: utf-8 -*-
#
# Condition plugin for command result
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import locale
from plugin import CommandConditionPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This tests a command by periodically running it in the background, and if
it succeeds (that is, it has an exit status of zero) the associated task
is run as a consequence. It can also run specially crafted scripts so that
virtually everything in the system can be checked.
""")


# class for a plugin: the derived class name should always be Plugin
class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename='cond-misc-command',
            name=_("Command"),
            description=_("Check successful execution of command"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='start',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-misc-command')
        self.plugin_panel = None
        self.forward_allowed = False
        self.command_line = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    # all following methods are optional

    def change_entry(self, obj):
        o = self.builder.get_object
        self.command_line = o('txtEntry').get_text()
        if self.command_line:
            command_name = os.path.basename(self.command_line.split()[0])
            self.summary_description = _(
                "After a command based on '%s' runs successfully") % command_name
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
