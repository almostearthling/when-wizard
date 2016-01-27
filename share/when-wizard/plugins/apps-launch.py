# file: share/when-wizard/modules/apps-launch.py
# -*- coding: utf-8 -*-
#
# Task plugin to launch an application
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

from plugin import TaskPlugin, CONST

import os
import sys
from glob import glob

from gi.repository import GLib, Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


SYSTEM_APPS_DIR = '/usr/share/applications'
USER_APPS_DIR = os.path.expanduser('~/.local/share/applications')


HELP = """\
Use this action to launch a desktop application: choose one from the list
and it will be started once the referring condition occurs. You will be
able to interact with the application and will have to close it yourself
when you finished using it.
"""

# desktop file format
# [Desktop Entry]
# Name=YouTube
# Type=Application
# Icon=unity-webapps-youtube
# MimeType=
# Actions=S0;S1;S2;S3;S4;S5;S6;S7;S8;S9;S10;
# Exec=unity-webapps-runner -n 'WW91VHViZQ==' -d 'youtube.com' %u
# StartupWMClass=YouTubeyoutubecom


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

    def list_applications(self):
        desktop_files = glob('%s/*.desktop' % SYSTEM_APPS_DIR)
        apps = []
        for filename in desktop_files:
            with open(filename) as f:
                icon = None
                name = None
                command = None
                for line in f:
                    values = line.split('=', 1)
                    entry = values[0].lower()
                    if entry == 'icon':
                        icon = values[1].strip()
                    elif entry == 'name':
                        name = values[1].strip()
                    elif entry == 'exec':
                        command = values[1].strip()
                if icon and name and command:
                    apps.append((name, filename, command, icon))
        return apps

    # see http://python-gtk-3-tutorial.readthedocs.org/en/latest/iconview.html
    def get_pane(self):
        if self.plugin_panel is None:
            # prepare panel and fill up application icons
            o = self.builder.get_object
            apps = self.list_applications()
            apps.sort()
            liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
            default_theme = Gtk.IconTheme.get_default()
            iconview = o('iconsApplications')
            # iconview.set_size_request(-1, 23)
            iconview.set_model(liststore)
            iconview.set_pixbuf_column(0)
            iconview.set_text_column(1)
            for app in apps:
                try:
                    pixbuf = default_theme.load_icon(app[3], 32, 0)
                except:
                    pixbuf = default_theme.load_icon('unknown', 32, 0)
                liststore.append([pixbuf, app[0], app[1]])
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

# end.
