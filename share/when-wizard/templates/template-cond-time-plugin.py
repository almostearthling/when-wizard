# file: share/when-wizard/templates/template-cond-time-plugin.py
# -*- coding: utf-8 -*-
#
# Condition plugin template
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import TimeConditionPlugin, PLUGIN_CONST

# Gtk might be needed: uncomment if this is the case
# from gi.repository import Gtk

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This is a template for a generic time plugin: it can be expanded suitably to
the needs of the plugin. A time plugin must provide a time specification that
specifies when in time the event should occur.
""")


# class for a plugin: the derived class name should always be Plugin
class Plugin(TimeConditionPlugin):

    def __init__(self):
        TimeConditionPlugin.__init__(
            self,
            basename='template-cond-time-plugin',
            name=_("Template"),
            description=_("Explain here what it does"),
            author="John Smith",
            copyright="Copyright (c) 2016",
            icon='puzzle',
            help_string=HELP,
        )
        # the items below might be not needed and can be deleted if the
        # plugin does not have a configuration panel
        self.builder = self.get_dialog('plugin_template')
        self.plugin_panel = None

        # mandatory or anyway structural variables and object values follow:
        # some of the timespec entries should be removed: if all are defined
        # the event will occur when time matches the whole definition, for
        # example, if a condition has to occur avery time that minute is 15
        # at every hour, the entries for year, month, day, hour and weekday
        # must be commented out or deleted
        self.timespec['year'] = 0
        self.timespec['month'] = 0
        self.timespec['day'] = 0
        self.timespec['hour'] = 0
        self.timespec['minute'] = 0
        self.timespec['weekday'] = 0
        self.summary_description = None     # must be set for all plugins

        # this variable is defined here only for demonstrational purposes
        self.value = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    # all following methods are optional

    def click_btnDo(self, obj):
        o = self.builder.get_object
        o('txtEntry').set_text("Some text")

    def change_entry(self, obj):
        o = self.builder.get_object
        self.value = o('txtEntry').get_text()
        if self.value:
            self.summary_description = _(
                "Something will be done with %s") % self.value
        else:
            self.summary_description = None


# end.
