# file: share/when-wizard/modules/power-hibernate.py
# -*- coding: utf-8 -*-
#
# Task plugin to enter hibernation
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
This action hibernates your Workstation, saving its current state and entering
a very low-consumption mode: depending on your OS release and your settings
the system will resume operations by either providing input or pressing the
power button. In some cases network activity could cause a wakeup.
""")


HIBERNATE_COMMAND = """dbus-send --system --dest=org.freedesktop.UPower \
/org/freedesktop/UPower org.freedesktop.UPower.Suspend"""
# HIBERNATE_COMMAND = """dbus-send --system --dest=org.freedesktop.UPower \
# /org/freedesktop/UPower org.freedesktop.UPower.Hibernate"""


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_POWER,
            basename='power-hibernate',
            name=_("Hibernate"),
            description=_("Hibernate your Workstation"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='night_landscape',
            help_string=HELP,
        )
        self.stock = True
        self.command_line = HIBERNATE_COMMAND
        self.summary_description = _("The system will be suspended/hibernated")


# end.
