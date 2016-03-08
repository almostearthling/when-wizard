# file: share/when-wizard/templates/cond-time-idletime.py
# -*- coding: utf-8 -*-
#
# Plugin to manage idle time condition
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import IdleConditionPlugin, PLUGIN_CONST, plugin_name

from resources import UI_INTERVALS_MINUTES, UI_INTERVALS_HOURS

locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
Run the associated task after the session has been idle for the specified
amount of time. The time can be given either in hours or in minutes.
""")


class Plugin(IdleConditionPlugin):

    def __init__(self):
        IdleConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Idle Time"),
            description=_("Occur when the workstation is idle"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='night_portrait',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-time-idletime')
        self.plugin_panel = None
        self.forward_allowed = False
        self.idlemins = None

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
                self.idlemins = value
            else:
                self.idlemins = value * 60
        except ValueError:
            self.idlemins = None
        if self.idlemins:
            if self.idlemins % 60:
                spec = str(self.idlemins) + _(" minutes")
            else:
                spec = str(int(self.idlemins / 60)) + _(" hours")
            self.summary_description = _(
                "After the computer has been idle for %s") % spec
            self.allow_forward(True)
        else:
            self.summary_description = None
            self.allow_forward(False)


# end.
