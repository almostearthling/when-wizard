# file: share/when-wizard/modules/cond-time-timeofday.py
# -*- coding: utf-8 -*-
#
# Task plugin to launch an application
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

from plugin import TimeConditionPlugin, CONST

import os
import sys
from glob import glob

from gi.repository import GLib, Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


HELP = """\
This pane allows to define the time of day when the condition will be
verified. Associated actions will occur every day at the specified time.
"""


class Plugin(TimeConditionPlugin):

    def __init__(self):
        TimeConditionPlugin.__init__(
            self,
            # category=CONST.CATEGORY_COND_TIME,
            basename='cond-time-timeofday',
            name='Time Of Day',
            description='Full Specification of the Time of Day',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='alarm_clock',
            help_string=HELP,
        )
        self.stock = True
        self.command_line = None
        self.plugin_panel = None
        self.builder = self.get_dialog('plugin_cond-time-timeofday')

    def get_pane(self, index=None):
        if self.plugin_panel is None:
            # prepare panel
            o = self.builder.get_object
            # ...
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel


# end.
