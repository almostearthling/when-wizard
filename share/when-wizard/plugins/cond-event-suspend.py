# file: share/when-wizard/templates/cond-event-cond-event-suspend.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session suspend event
# Copyright (c) 2015-2016 Francesco Garosi
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
This event will occur when the session suspends or the computer enters
hibernation mode, that is a very low energy consumption mode that saves
the session state to resume it later exactly where it left. Consider that
the result of the event may take place after the system has resumed.
""")


EVENT_SYSTEM_SUSPEND = 'system_suspend'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Suspend"),
            description=_("Enter a low consumption mode"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='night_landscape',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_POWER
        self.stock = True
        self.event = EVENT_SYSTEM_SUSPEND
        self.summary_description = _("When the session is suspended")


# end.
