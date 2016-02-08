# file: share/when-wizard/templates/cond-event-batterydischarging.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the battery discharging event
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
This event will occur when the battery is discharging, for example when you
use a notebook and plug it off the mains socket.
""")


EVENT_SYSTEM_BATTERY_DISCHARGING = 'battery_discharging'


# class for a plugin: the derived class name should always be Plugin
class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename='cond-event-batterydischarging',
            name=_("Discharging"),
            description=_("The Battery is Discharging"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='high_battery',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        # mandatory or anyway structural variables and object values follow:
        self.stock = True
        self.event = EVENT_SYSTEM_BATTERY_DISCHARGING
        self.summary_description = _("When the battery is discharging")


# end.
