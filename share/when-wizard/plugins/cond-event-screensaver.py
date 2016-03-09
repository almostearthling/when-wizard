# file: share/when-wizard/templates/cond-event-screensaver.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the screen saver start event
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
This event will occur when the screensaver starts, which normally happens
when the workstation has been idle for a while. The idle time before the
screensaver starts can be defined in the user settings.
""")


EVENT_SESSION_SCREENSAVER = 'screensaver'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Screensaver"),
            description=_("The Screensaver Starts"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='panorama',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.event = EVENT_SESSION_SCREENSAVER
        self.summary_description = _("When the screensaver starts")


# end.
