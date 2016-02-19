# file: share/when-wizard/lib/utility.py
# -*- coding: utf-8 -*-
#
# Generic utilities
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import sys
import time
import dbus

from gi.repository import Gtk


from datastore import PicklingDatastore


datastore = PicklingDatastore()
datastore.filename = os.path.join(USER_STORE_FOLDER, 'when-wizard.datastore')


# constants for DBus communication
_WHEN_COMMAND_ID = 'it.jks.WhenCommand'
_WHEN_COMMAND_BUS_NAME = '%s.BusService' % _WHEN_COMMAND_ID
_WHEN_COMMAND_BUS_PATH = '/' + _WHEN_COMMAND_BUS_NAME.replace('.', '/')


# the configuration options to make the When applet a suitable companion
WHEN_OPTIONS_GENERIC = {
    'General': {
        'show icon': True,
        'autostart': True,
        'notifications': False,
        'user events': True,
        'file notifications': True,
        'minimalistic mode': True,
    },
    'Scheduler': {
        'preserve pause': True,
    }
}

# configuration options for scheduler reactivity
WHEN_OPTIONS_REACTIVITY_NORMAL = {
    'Scheduler': {
        'tick seconds': 15,
        'skip seconds': 60,
    }
}

WHEN_OPTIONS_REACTIVITY_LAZY = {
    'Scheduler': {
        'tick seconds': 60,
        'skip seconds': 300,
    }
}


# constants for desktop entries
APP_ENTRY_DESKTOP = """\
#!/usr/bin/env xdg-open
[Desktop Entry]
Version={version}
Name={app_name}
Comment={app_comment}
Icon={icon_path}/{icon_name}.png
Terminal=false
Type=Application
Categories=Utility;Application;System;
Exec={loader_exec} {subcommand}
"""


# format an exception for logging purposes
# def _x(e):
#     t, v, tb = sys.exc_info()
#     if t is None:
#         return ''
#     return '%s: %s' % (t.__name__, v)


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
        order = [USER_RESOURCE_FOLDER, APP_RESOURCE_FOLDER]
    else:
        order = [APP_RESOURCE_FOLDER, USER_RESOURCE_FOLDER]
    if PLUGIN_TEMP_FOLDER:
        order.insert(0, PLUGIN_TEMP_FOLDER)
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
        order = [USER_RESOURCE_FOLDER, APP_ICONS_FOLDER, APP_GRAPHICS_FOLDER]
    else:
        order = [APP_ICONS_FOLDER, APP_GRAPHICS_FOLDER, USER_RESOURCE_FOLDER]
    if PLUGIN_TEMP_FOLDER:
        order.insert(0, PLUGIN_TEMP_FOLDER)
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


# specific function for application dialog boxes
def app_dialog(name):
    with open(os.path.join(APP_RESOURCE_FOLDER, '%s.glade' % name)) as f:
        dialog_xml = f.read()
    return dialog_xml


# an utility function that creates an unique string of fixed length
def unique_str():
    return hex(int(time.time() * 1000000000))[2:]


# return a proxy to the remote DBus interface of the When applet, if running
def when_proxy():
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object(_WHEN_COMMAND_BUS_NAME, _WHEN_COMMAND_BUS_PATH)
        return proxy
    except dbus.exceptions.DBusException:
        return None


# apply options, passed as a list of dictionaries, to a running When instance
def when_apply_options(dicts):
    proxy = when_proxy()
    if proxy is None:
        return False
    try:
        for d in dicts:
            for section in d:
                for entry in d[section]:
                    value = d[section][entry]
                    proxy.SetConfig(section, entry, value, False)
    except dbus.exceptions.DBusException:
        return False
    try:
        proxy.ReloadConfig()
    except dbus.exceptions.DBusException:
        return False
    return True


def write_desktop_entry(subcommand, appname, iconname, comment=APP_LONGDESC):
    if APP_BIN_FOLDER.startswith('/usr'):
        return False
    contents = APP_ENTRY_DESKTOP.format(
        version=APP_VERSION,
        app_name=appname,
        app_comment=comment,
        icon_name=iconname,
        subcommand=subcommand,
        loader_exec=os.path.join(APP_BIN_FOLDER, APP_NAME),
        icon_path=APP_GRAPHICS_FOLDER,
    )
    filename = os.path.join(USER_LAUNCHER_FOLDER, '%s.desktop' % subcommand)
    try:
        with open(filename, 'w') as f:
            f.write(contents)
    except IOError:
        return False
    return True


# end.
