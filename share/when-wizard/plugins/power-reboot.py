# file: share/when-wizard/modules/power-reboot.py
# -*- coding: utf-8 -*-
#
# Task plugin to reboot the system
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
This action reboots your Workstation, exactly in the same way as you would
do using the session shutdown menu. Your computer closes all applications and
flushes all data to disk to enable a clean restart, however be sure that your
data is saved (or at least auto-saved) before letting the computer restart.
""")


REBOOT_COMMAND = ""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_POWER,
            basename='power-reboot',
            name=_("Reboot"),
            description=_("Reboot your Workstation"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='refresh',
            help_string=HELP,
        )
        self.stock = True
        self.command_line = REBOOT_COMMAND


# end.
