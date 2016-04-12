# file: share/when-wizard/templates/cond-misc-sysload.py
# -*- coding: utf-8 -*-
#
# Template for a command based condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import locale
from plugin import CommandConditionPlugin, PLUGIN_CONST, plugin_name

# Gtk might be needed: uncomment if this is the case
# from gi.repository import Gtk


# setup localization for both plugin text and configuration pane
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
The current system load is compared against a given target percentage: if
higher than the target, the associated consequence is triggered.
""")

PERCENTAGES = [10, 25, 50, 70, 80, 90, 100, 150, 200, 300]


# class for a plugin: the derived class name should always be Plugin
class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("System Load"),
            description=_("Check system load against a target"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='electronics',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.repeat = True
        self.builder = self.get_dialog('plugin_cond-misc-sysload')
        self.plugin_panel = None
        self.forward_allowed = False
        self.command_line = None
        self.summary_description = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            cbPercentage = o('cbPercentage')
            cbPercentage.get_model().clear()
            for x in PERCENTAGES:
                cbPercentage.append_text(str(x))
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        try:
            value = int(o('txtPercentage').get_text())
            if value < 1:
                value = None
        except TypeError:
            value = None
        if value:
            self.summary_description = _("When CPU load reaches %s%%") % value
            self.command_line = "%s %s" % (
                self.get_script('plugin_cond-misc-sysload.sh'), value)
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
