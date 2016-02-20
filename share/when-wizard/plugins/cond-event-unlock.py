# file: share/when-wizard/templates/cond-event-unlock.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session unlock event
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will occur when you unlock the session.
""")


EVENT_SESSION_UNLOCK = 'session_unlock'


# class for a plugin: the derived class name should always be Plugin
class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename='cond-event-unlock',
            name=_("Session Unlock"),
            description=_("Unlock the User Session"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='unlock',
            help_string=HELP,
            version=APP_VERSION,
        )
        # mandatory or anyway structural variables and object values follow:
        self.stock = True
        self.event = EVENT_SESSION_UNLOCK
        self.summary_description = _("When the session is unlocked")


# end.
