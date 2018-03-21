# file: share/when-wizard/templates/cond-misc-systemp.py
# -*- coding: utf-8 -*-
#
# Check current system temperature against a target
# Copyright (c) 2015-2018 Francesco Garosi
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
The current system temperature is compared against a given target Celsius
value: if higher than the target, the associated consequence is triggered.
""")

TEMPS = [30, 40, 50, 60, 70, 80, 90, 100]


# class for a plugin: the derived class name should always be Plugin
class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("System Temperature"),
            description=_("Check system temperature against a target"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='electrical_sensor',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.repeat = True
        self.builder = self.get_dialog('plugin_cond-misc-systemp')
        self.plugin_panel = None
        self.forward_allowed = False
        self.command_line = None
        self.summary_description = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            cbTemp = o('cbTemp')
            cbTemp.get_model().clear()
            for x in TEMPS:
                cbTemp.append_text(str(x))
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        try:
            value = int(o('txtTemp').get_text())
            if value < 0:
                value = None
        except TypeError:
            value = None
        if value:
            self.summary_description = _("When system temperature reaches %s°C") % value
            self.command_line = "%s %s" % (
                self.get_script('plugin_cond-misc-systemp.sh'), value)
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
