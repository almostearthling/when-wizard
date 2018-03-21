# file: share/when-wizard/plugins/misc-keystroke.py
# -*- coding: utf-8 -*-
#
# Plugin to send a keystroke to a running application if present
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Wnck', '3.0')
from gi.repository import Gtk, Wnck

import locale
from plugin import TaskPlugin, PLUGIN_CONST, plugin_name


# setup localization for both plugin text and configuration pane
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This action allows to choose the title of a windowed application and send a
keystroke to it: if the application is not running or not found the action
is ignored and no keystroke is sent. Specify keystrokes as strings, such as
'ctrl+c', 'alt+f4', 'esc', and so on: bad specifications result in errors.
""")


# xdotool appears to be a very interesting utility to build tasks: see website
# and documentation at http://www.semicomplete.com/projects/xdotool/
cmd_template = \
    "xdotool search '%s' windowactivate --sync key --clearmodifiers '%s'"


# class for a plugin: the derived class name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_MISC,
            basename=plugin_name(__file__),
            name=_("Send Keystroke"),
            description=_("Send a keystroke to an open window"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='internal',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_misc-keystroke')
        self.plugin_panel = None
        self.forward_allowed = False
        self.command_line = None
        self.summary_description = None
        self.window_title = None
        self.keystroke = None

    # see http://stackoverflow.com/a/16703307/5138770 for window list
    def get_pane(self):
        o = self.builder.get_object
        if self.plugin_panel is None:
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        screen = Wnck.Screen.get_default()
        screen.force_update()
        li = []
        for window in screen.get_windows():
            li.append(window.get_name())
        cb = o('cbWindowTitle')
        cb.get_model().clear()
        if li:
            li.sort()
            for x in li:
                cb.append_text(x)
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        self.window_title = o('txtWindowTitle').get_text()
        self.keystroke = o('txtKeyStroke').get_text().lower()
        if self.window_title and self.keystroke:
            self.command_line = cmd_template % (self.window_title,
                                                self.keystroke)
            self.summary_description = _(
                "Keystroke %s will be sent to '%s'") % (self.keystroke,
                                                        self.window_title)
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
