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


# TODO: find the suitable command to reboot
REBOOT_COMMAND = "gnome-session-quit --no-prompt --reboot"


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
            version="0.1~alpha.0",
        )
        self.stock = True
        self.command_line = REBOOT_COMMAND
        self.summary_description = _("The system will be rebooted")


# end.
