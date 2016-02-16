# file: share/when-wizard/templates/cond-time-interval.py
# -*- coding: utf-8 -*-
#
# Time interval condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import IntervalConditionPlugin, PLUGIN_CONST

from resources import UI_INTERVALS_MINUTES, UI_INTERVALS_HOURS

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
Run the associated task whenever a certain interval of time has passed:
the time can be specified as an amount of either minutes or hours, and
time accounting begins as soon as the scheduler starts.
""")


class Plugin(IntervalConditionPlugin):

    def __init__(self):
        IntervalConditionPlugin.__init__(
            self,
            basename='cond-time-interval',
            name=_("Time Interval"),
            description=_("Occur periodically after an amount of time"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='pie_chart',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-time-interval')
        self.plugin_panel = None
        self.forward_allowed = False
        self.interval = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
            o('cbValue').get_model().clear()
            for x in UI_INTERVALS_MINUTES:
                o('cbValue').append_text(str(x))
        return self.plugin_panel

    def change_unit(self, obj):
        o = self.builder.get_object
        idx = o('cbUnit').get_selected()
        if idx == 0:
            l = UI_INTERVALS_MINUTES
        else:
            l = UI_INTERVALS_HOURS
        o('cbValue').get_model().clear()
        for x in l:
            o('cbValue').append_text(str(x))

    def change_entry(self, obj):
        o = self.builder.get_object
        idx = o('cbUnit').get_active()
        try:
            value = int(o('txtValue').get_text())
            if idx == 0:
                self.interval = value
            else:
                self.interval = value * 60
        except ValueError:
            self.interval = None
        if self.interval:
            if self.interval % 60:
                spec = str(self.interval) + _(" minutes")
            else:
                spec = str(int(self.interval / 60)) + _(" hours")
            self.summary_description = _(
                "The event will occur every %s") % spec
            self.allow_forward(True)
        else:
            self.summary_description = None
            self.allow_forward(False)


# end.
