# file: share/when-wizard/modules/cond-time-timeofday.py
# -*- coding: utf-8 -*-
#
# Plugin for time based condition
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import TimeConditionPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This pane allows to define the time of day when the condition will be
verified. Associated actions will occur every day at the specified time.
""")


class Plugin(TimeConditionPlugin):

    def __init__(self):
        TimeConditionPlugin.__init__(
            self,
            basename='cond-time-timeofday',
            name=_("Time Of Day"),
            description=_("Full Specification of the Time of Day"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='alarm_clock',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-time-timeofday')
        self.plugin_panel = None
        self.timespec['hour'] = 0
        self.timespec['minute'] = 0
        self.summary_description = _("At midnight")
        self.forward_allowed = True

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            o('spinHour').set_text(str(self.timespec['hour']))
            o('spinMinute').set_text(str(self.timespec['minute']))
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_spins(self, o):
        o = self.builder.get_object
        self.timespec['hour'] = int(o('spinHour').get_text())
        self.timespec['minute'] = int(o('spinMinute').get_text())
        shr = ("00" + str(self.timespec['hour']))[-2:]
        smin = ("00" + str(self.timespec['minute']))[-2:]
        self.summary_description = _(
            "At %s:%s o'clock") % (shr, smin)
        self.allow_forward(True)


# end.
