# file: share/when-wizard/modules/cond-time-full.py
# -*- coding: utf-8 -*-
#
# Plugin for time based condition
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import TimeConditionPlugin, PLUGIN_CONST, plugin_name
import time

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This pane allows to define the exact time specification when the condition
will be verified. Associated actions will occur at the specified time.
""")


class Plugin(TimeConditionPlugin):

    def __init__(self):
        TimeConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Date and Time"),
            description=_("Full Specification of Date and Time"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='calendar',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-time-full')
        self.plugin_panel = None
        t = time.localtime()
        self.timespec['hour'] = 0
        self.timespec['minute'] = 0
        self.timespec['year'] = t.tm_year
        self.timespec['month'] = t.tm_mon
        self.timespec['day'] = t.tm_mday
        self.summary_description = _("Today at midnight")
        self.forward_allowed = True

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            o('spinHour').set_text(str(self.timespec['hour']))
            o('spinMinute').set_text(str(self.timespec['minute']))
            cal = o('calDate')
            cal.select_month(self.timespec['month'] - 1, self.timespec['year'])
            cal.select_day(self.timespec['day'])
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_spins(self, o):
        o = self.builder.get_object
        self.timespec['hour'] = int(o('spinHour').get_text())
        self.timespec['minute'] = int(o('spinMinute').get_text())
        shr = ("00" + str(self.timespec['hour']))[-2:]
        smin = ("00" + str(self.timespec['minute']))[-2:]
        cal = o('calDate')
        year, month, day = cal.get_date()
        month += 1
        self.timespec['year'] = year
        self.timespec['month'] = month
        self.timespec['day'] = day
        self.summary_description = _("On %s/%s/%s at %s:%s o'clock") % (
            year, month, day, shr, smin)
        self.allow_forward(True)


# end.
