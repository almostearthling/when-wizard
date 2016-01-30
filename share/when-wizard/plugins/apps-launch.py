# file: share/when-wizard/modules/apps-launch.py
# -*- coding: utf-8 -*-
#
# Task plugin to launch an application
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

from plugin import TaskPlugin, CONST

import os
import sys

# from gi.repository import GLib, Gio
# from gi.repository import GObject
# from gi.repository import Gtk
# from gi.repository import Gdk
# from gi.repository import GdkPixbuf


HELP = """\
Use this action to launch a desktop application: choose one from the list
and it will be started once the referring condition occurs. You will be
able to interact with the application and will have to close it yourself
when you finished using it.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_APPS,
            basename='apps-launch',
            name='Application Launcher',
            description='Start an Application',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='electro_devices',
            help_string=HELP,
        )
        self.stock = True
        self.command_line = None
        self.plugin_panel = None
        self.builder = self.get_dialog('plugin_apps-launch')

    # see http://python-gtk-3-tutorial.readthedocs.org/en/latest/iconview.html
    def get_pane(self, index=None):
        if self.plugin_panel is None:
            o = self.builder.get_object
            o('appChooser').set_show_all(True)
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def select_application(self, o, desktop_app):
        desktop_filename = desktop_app.get_filename()
        self.command_line = '%s run-desktop %s' % (
            os.path.join(APP_BIN_FOLDER, 'when-wizard'), desktop_filename)


# end.
