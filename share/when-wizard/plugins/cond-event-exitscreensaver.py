# file: share/when-wizard/templates/cond-event-exitscreensaver.py
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
This event will occur when the screensaver exits, which normally happens
when there is user interaction while the screensaver is active.
""")


EVENT_APPLET_STARTUP = 'startup'
EVENT_APPLET_SHUTDOWN = 'shutdown'
EVENT_SYSTEM_SUSPEND = 'system_suspend'
EVENT_SYSTEM_RESUME = 'system_resume'
EVENT_SYSTEM_DEVICE_ATTACH = 'device_attach'
EVENT_SYSTEM_DEVICE_DETACH = 'device_detach'
EVENT_SYSTEM_NETWORK_JOIN = 'network_join'
EVENT_SYSTEM_NETWORK_LEAVE = 'network_leave'
EVENT_SESSION_SCREENSAVER = 'screensaver'
EVENT_SESSION_SCREENSAVER_EXIT = 'screensaver_exit'
EVENT_SESSION_LOCK = 'session_lock'
EVENT_SESSION_UNLOCK = 'session_unlock'
EVENT_COMMAND_LINE = 'command_line'
EVENT_SYSTEM_BATTERY_CHARGE = 'battery_charge'
EVENT_SYSTEM_BATTERY_DISCHARGING = 'battery_discharging'
EVENT_SYSTEM_BATTERY_LOW = 'battery_low'


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
