# file: share/when-wizard/modules/apps-command.py
# -*- coding: utf-8 -*-
#
# Task plugin to start a command
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

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


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_APPS,
            basename='apps-command',
            name=_("Command Launcher"),
            description=_("Start a System Command"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='start',
            help_string=HELP,
        )
        self.stock = True


# end.
