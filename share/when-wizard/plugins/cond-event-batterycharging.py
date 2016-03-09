# file: share/when-wizard/templates/cond-event-batterycharging.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the battery charging event
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
This event will occur when the battery is charging, for example when you
use a notebook and plug it in the mains socket.
""")


EVENT_SYSTEM_BATTERY_CHARGE = 'battery_charge'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Charging"),
            description=_("The Battery is Charging"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='charge_battery',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_POWER
        self.stock = True
        self.event = EVENT_SYSTEM_BATTERY_CHARGE
        self.summary_description = _("When the battery is charging")


# end.
