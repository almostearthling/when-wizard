# file: share/when-wizard/modules/power-hibernate.py
# -*- coding: utf-8 -*-
#
# Task plugin to enter hibernation
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import TaskPlugin, PLUGIN_CONST, plugin_name

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


HIBERNATE_COMMAND = """\
sleep 2 && \
gdbus call -y -d org.freedesktop.UPower \
              -o /org/freedesktop/UPower \
              -m org.freedesktop.UPower.Suspend
"""


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_POWER,
            basename=plugin_name(__file__),
            name=_("Hibernate"),
            description=_("Hibernate your Workstation"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='night_landscape',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.command_line = HIBERNATE_COMMAND
        self.summary_description = _("The system will suspend or hibernate")


# end.
