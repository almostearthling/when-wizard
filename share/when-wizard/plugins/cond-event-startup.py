# file: share/when-wizard/templates/cond-event-startup.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session startup event
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name

# Gtk might be needed: uncomment if this is the case
# from gi.repository import Gtk

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will occur as soon as the applet is started, normally when the
session itself begins, that is at login time or after the computer was
turned on.
""")


EVENT_APPLET_STARTUP = 'startup'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Session Start"),
            description=_("Beginning of the User Session"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='sports_mode',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.event = EVENT_APPLET_STARTUP
        self.summary_description = _("When the session is beginning")


# end.
