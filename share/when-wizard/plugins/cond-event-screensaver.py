# file: share/when-wizard/templates/cond-event-screensaver.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the screen saver start event
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
This event will occur when the session locks, either because the system is
instructed to do so after a while or because you intentionally locked your
computer by pressing the lock key combination or by selecting an appropriate
menu entry.
""")


EVENT_SESSION_SCREENSAVER = 'screensaver'


# class for a plugin: the derived class name should always be Plugin
class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename='cond-event-screensaver',
            name=_("Screensaver"),
            description=_("The Screensaver Starts"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='panorama',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        # mandatory or anyway structural variables and object values follow:
        self.stock = True
        self.event = EVENT_SESSION_SCREENSAVER
        self.summary_description = _("When the screensaver starts")


# end.
