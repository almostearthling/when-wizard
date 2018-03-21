# file: share/when-wizard/modules/power-reboot.py
# -*- coding: utf-8 -*-
#
# Task plugin to reboot the system
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)
# NOTE: the consolekit package is a *mandatory* requirement

import locale
from plugin import TaskPlugin, PLUGIN_CONST, plugin_name

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


# see: http://superuser.com/a/533684/471608
# I also like `gdbus` as a command, it is probably more gnome-ish;
# the reason for the one-minute sleep is that the user may want to do
# something before shutting down, such as write an e-mail or send a message
# through another action
REBOOT_COMMAND = """\
sleep 60 && \
gdbus call -y -d org.freedesktop.ConsoleKit \
              -o /org/freedesktop/ConsoleKit/Manager \
              -m org.freedesktop.ConsoleKit.Manager.Restart
"""


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_POWER,
            basename=plugin_name(__file__),
            name=_("Reboot"),
            description=_("Reboot your Workstation"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='refresh',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.command_line = REBOOT_COMMAND
        self.summary_description = _("The system will reboot")


# end.
