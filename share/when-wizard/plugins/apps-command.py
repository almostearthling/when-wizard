# file: share/when-wizard/modules/apps-command.py
# -*- coding: utf-8 -*-
#
# Task plugin to start a command
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import locale
from plugin import TaskPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This task is used to start a non-interactive system command: you can provide
the whole command line that will be executed in the background without user
interaction.
""")


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_APPS,
            basename='apps-command',
            name=_("Command Launcher"),
            description=_("Run a Command using the default Shell"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='start',
            help_string=HELP,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_apps-command')
        self.plugin_panel = None
        self.forward_allowed = False

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_command(self, obj):
        o = self.builder.get_object
        self.command_line = o('txtCommand').get_text()
        if self.command_line:
            command_name = os.path.basename(self.command_line.split()[0])
            self.summary_description = _(
                "A command based on '%s' will be run") % command_name
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
