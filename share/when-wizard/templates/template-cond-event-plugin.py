# file: share/when-wizard/templates/template-cond-event-plugin.py
# -*- coding: utf-8 -*-
#
# Template for an event condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name


# setup localization for both plugin text and configuration pane
# locale.setlocale(locale.LC_ALL, locale.getlocale())
# locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
# locale.textdomain(APP_NAME)
# _ = locale.gettext

# if localization is supported, uncomment the lines above configure
# them as appropriate, and remove this replacement function
def _(x):
    return x


HELP = _("""\
This is a template for a generic event condition plugin: it can be expanded
suitably to the needs of the plugin. An event condition plugin must only
provide the observed event as one of the constants defined below. Conditions
that watch events have no configuration, thus they show no pane.
""")


EVENT_APPLET_STARTUP = 'startup'
EVENT_APPLET_SHUTDOWN = 'shutdown'
EVENT_SYSTEM_SUSPEND = 'system_suspend'
EVENT_SYSTEM_RESUME = 'system_resume'
EVENT_SYSTEM_DEVICE_ATTACH = 'device_attach'
EVENT_SYSTEM_DEVICE_DETACH = 'device_detach'
EVENT_SYSTEM_NETWORK_JOIN = 'network_join'
EVENT_SYSTEM_NETWORK_LEAVE = 'network_leave'
EVENT_SESSION_SCREENSAVER = 'screensaver'
EVENT_SESSION_SCREENSAVER_EXIT = 'screensaver_exit'
EVENT_SESSION_LOCK = 'session_lock'
EVENT_SESSION_UNLOCK = 'session_unlock'
EVENT_COMMAND_LINE = 'command_line'
EVENT_SYSTEM_BATTERY_CHARGE = 'battery_charge'
EVENT_SYSTEM_BATTERY_DISCHARGING = 'battery_discharging'
EVENT_SYSTEM_BATTERY_LOW = 'battery_low'


# class for a plugin: the derived class name should always be Plugin
class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Template"),
            description=_("Explain here what it does"),
            author="John Smith",
            copyright="Copyright (c) 2016",
            icon='puzzle',
            help_string=HELP,
            version="0.1.0",
        )
        # the icon resource is only needed if the plugin uses a custom icon
        # self.graphics.append('plugin_icon.png')

        # define this only if the plugin provides one or more scripts
        # self.scripts.append('needed_script.sh')

        # mandatory or anyway structural variables and object values follow:
        self.event = EVENT_CONSTANT         # this has to be changed
        self.summary_description = None     # has to be set to a fixed string


# end.
