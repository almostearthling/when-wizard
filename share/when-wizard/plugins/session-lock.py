# file: share/when-wizard/modules/session-lock.py
# -*- coding: utf-8 -*-
#
# Task plugin to lock the session
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
This task locks your session without logging you out: it protects your
Workstation by asking for a password to start over to work, but does not
close any application.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_SESSION,
            basename='session-lock',
            name=_("Lock"),
            description=_("Session Lock"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='lock',
            help_string=HELP,
        )
        self.stock = True


# end.
