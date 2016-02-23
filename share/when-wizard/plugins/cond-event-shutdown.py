# file: share/when-wizard/templates/cond-event-shutdown.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session close event
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST

# Gtk might be needed: uncomment if this is the case
# from gi.repository import Gtk

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will occur as soon as the applet is closed, normally when the
session itself finishes, at logout or when the computer is shut down. It is
not safe to perform heavy operations here, because on real shutdown only a
one second grace time is left to applications.
""")


EVENT_APPLET_SHUTDOWN = 'shutdown'


# class for a plugin: the derived class name should always be Plugin
class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename='cond-event-shutdown',
            name=_("Session End"),
            description=_("End of the User Session"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='no_idea',
            help_string=HELP,
            version=APP_VERSION,
        )
        # mandatory or anyway structural variables and object values follow:
        self.stock = True
        self.event = EVENT_APPLET_SHUTDOWN
        self.summary_description = _("When the session is ending")


# end.
