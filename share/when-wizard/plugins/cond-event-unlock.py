# file: share/when-wizard/templates/cond-event-unlock.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session unlock event
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will occur when the session exits from locked state, by entering
the correct password in the lock screen.
""")


EVENT_SESSION_UNLOCK = 'session_unlock'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Session Unlock"),
            description=_("Unlock the User Session"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='unlock',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.event = EVENT_SESSION_UNLOCK
        self.summary_description = _("When the session is unlocked")


# end.
