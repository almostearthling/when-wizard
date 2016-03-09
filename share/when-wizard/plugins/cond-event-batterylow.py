# file: share/when-wizard/templates/cond-event-batterylow.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the low battery event
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
This event will occur when the battery is considered critically low by the
system: use this only if the event is not caught by the system itself, for
example by hibernating the computer.
""")


EVENT_SYSTEM_BATTERY_LOW = 'battery_low'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Low Battery"),
            description=_("The Battery is Critically Low"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='low_battery',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_POWER
        self.stock = True
        self.event = EVENT_SYSTEM_BATTERY_LOW
        self.summary_description = _("When the battery is critically low")


# end.
