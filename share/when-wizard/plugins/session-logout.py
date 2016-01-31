# file: share/when-wizard/modules/session-logout.py
# -*- coding: utf-8 -*-
#
# Task plugin to log out from session
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
This task logs you out from the workstation. It closes all applications and
your desktop session, returning to the login screen. Be careful when you use
this task, because when it occurs you are likely to loose any unsaved work.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_SESSION,
            basename='session-logout',
            name=_("Logout"),
            description=_("Session Logout"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='undo',
            help_string=HELP,
        )
        self.stock = True


# end.
