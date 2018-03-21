# file: share/when-wizard/templates/cond-event-lock.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session lock event
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will occur when the session locks, either because the system is
instructed to do so after a while or because you intentionally locked your
computer by pressing the lock key combination or by selecting an appropriate
menu entry.
""")


EVENT_SESSION_LOCK = 'session_lock'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Session Lock"),
            description=_("Lock the User Session"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='lock',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.event = EVENT_SESSION_LOCK
        self.summary_description = _("When the session is being locked")


# end.
