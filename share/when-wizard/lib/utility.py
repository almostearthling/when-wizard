# file: share/when-wizard/lib/utility.py
# -*- coding: utf-8 -*-
#
# Generic utilities
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import sys
import time

from gi.repository import Gtk


from datastore import PicklingDatastore


datastore = PicklingDatastore()
datastore.filename = os.path.join(USER_STORE_FOLDER, 'when-wizard.datastore')


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
    if not os.path.exists(USER_RESOURCE_FOLDER):
        os.makedirs(USER_RESOURCE_FOLDER, exist_ok=True)
    if not os.path.exists(USER_SCRIPT_FOLDER):
        os.makedirs(USER_SCRIPT_FOLDER, exist_ok=True)


# retrieve dialog design resources using a custom directory search order
def load_dialog(name, reverse_order=False):
    if reverse_order:
        order = USER_RESOURCE_FOLDER, APP_RESOURCE_FOLDER
    else:
        order = APP_RESOURCE_FOLDER, USER_RESOURCE_FOLDER
    for path in order:
        for ext in ['glade', 'ui']:
            filename = os.path.join(path, '%s.%s' % (name, ext))
            if os.path.exists(filename):
                with open(filename) as f:
                    dialog_xml = f.read()
                    return dialog_xml
    return None


def build_dialog(name, reverse_order=False):
    dialog_xml = load_dialog(name, reverse_order)
    if dialog_xml:
        return Gtk.Builder().new_from_string(dialog_xml, -1)
    else:
        return None


# retrieve images from files using a custom directory search order
def load_icon(name, reverse_order=False):
    if reverse_order:
        order = USER_RESOURCE_FOLDER, APP_GRAPHICS_FOLDER
    else:
        order = APP_GRAPHICS_FOLDER, USER_RESOURCE_FOLDER
    for path in order:
        filename = os.path.join(path, '%s.png' % name)
        if os.path.exists(filename):
            image = Gtk.Image.new_from_file(filename)
            return image
    return None


def load_pixbuf(name, reverse_order=False):
    image = load_icon(name, reverse_order)
    if image:
        return image.get_pixbuf()
    else:
        return None


# specific function for application specific icons and resources
def app_dialog_from_name(name):
    with open(os.path.join(APP_RESOURCE_FOLDER, '%s.glade' % name)) as f:
        dialog_xml = f.read()
    return dialog_xml


def app_icon_from_name(name, size=24):
    appicon_dir = os.path.join(APP_GRAPHICS_FOLDER, 'app-icons', str(size))
    appicon_file = os.path.join(appicon_dir, '%s.png' % name)
    if not os.path.exists(appicon_file):
        return None
    image = Gtk.Image.new_from_file(appicon_file)
    return image


def app_pixbuf_from_name(name, size=24):
    image = app_icon_from_name(name, size)
    if image:
        return image.get_pixbuf()
    else:
        return None


# an utility function that creates an unique string of fixed length
def unique_str():
    return hex(int(time.time() * 1000000000))[2:]


# end.
