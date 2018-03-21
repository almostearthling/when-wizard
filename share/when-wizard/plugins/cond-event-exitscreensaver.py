# file: share/when-wizard/templates/cond-event-exitscreensaver.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the screen saver start event
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
This event will occur when the screensaver exits, which normally happens
when there is user interaction while the screensaver is active.
""")


EVENT_SESSION_SCREENSAVER_EXIT = 'screensaver_exit'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Exit Screensaver"),
            description=_("The Screensaver Ends"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='light_at_the_end_of_tunnel',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.event = EVENT_SESSION_SCREENSAVER_EXIT
        self.summary_description = _("When the screensaver stops")


# end.
