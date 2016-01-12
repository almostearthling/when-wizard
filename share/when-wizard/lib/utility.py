# file: share/when-wizard/modules/utility.py
# -*- coding: utf-8 -*-
#
# Generic utilities
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import sys

from gi.repository import GLib, Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango


# format an exception for logging purposes
def _x(e):
    t, v, tb = sys.exc_info()
    if t is None:
        return ''
    return '%s: %s' % (t.__name__, v)


# verify that the user folders are present, otherwise create them
def verify_user_folders():
    if not os.path.exists(USER_DATA_FOLDER):
        os.makedirs(USER_DATA_FOLDER, exist_ok=True)
    if not os.path.exists(USER_CONFIG_FOLDER):
        os.makedirs(USER_CONFIG_FOLDER, exist_ok=True)
    if not os.path.exists(USER_LAUNCHER_FOLDER):
        os.makedirs(USER_LAUNCHER_FOLDER, exist_ok=True)
    if not os.path.exists(USER_STORE_FOLDER):
        os.makedirs(USER_STORE_FOLDER, exist_ok=True)
    if not os.path.exists(USER_PLUGIN_FOLDER):
        os.makedirs(USER_PLUGIN_FOLDER, exist_ok=True)


def load_app_dialog(name):
    base = os.path.dirname(sys.argv[0])
    with open(os.path.join(APP_RESOURCE_FOLDER, '%s.glade' % name)) as f:
        dialog_xml = f.read()
    return dialog_xml


# images from files
def app_icon_from_name(name, size=24):
    appicon_dir = os.path.join(APP_GRAPHICS_FOLDER, 'app-icons', str(size))
    appicon_file = os.path.join(appicon_dir, '%s.png' % name)
    if not os.path.exists(appicon_file):
        return None
    image = Gtk.Image.new_from_file(appicon_file)
    return image


def app_pixbuf_from_name(name, size=24):
    appicon_dir = os.path.join(APP_GRAPHICS_FOLDER, 'app-icons', str(size))
    appicon_file = os.path.join(appicon_dir, '%s.png' % name)
    if not os.path.exists(appicon_file):
        return None
    image = Gtk.Image.new_from_file(appicon_file)
    return image.get_pixbuf()


# end.
