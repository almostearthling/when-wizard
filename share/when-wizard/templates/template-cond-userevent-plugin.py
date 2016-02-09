# file: share/when-wizard/templates/template-cond-userevent-plugin.py
# -*- coding: utf-8 -*-
#
# Template for an user defined event condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import UserEventConditionPlugin, PLUGIN_CONST


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
This is a template for an user event condition plugin: it can be expanded
suitably to the needs of the plugin. Such event condition plugin must only
provide the observed event name as imported into the applet. Conditions
that watch events have no configuration, thus they show no pane.
""")


# class for a plugin: the derived class name should always be Plugin
class Plugin(UserEventConditionPlugin):

    def __init__(self):
        UserEventConditionPlugin.__init__(
            self,
            basename='template-cond-userevent-plugin',
            name=_("Template"),
            description=_("Explain here what it does"),
            author="John Smith",
            copyright="Copyright (c) 2016",
            icon='puzzle',
            help_string=HELP,
            version="0.1.0",
        )
        # mandatory or anyway structural variables and object values follow:
        self.event_name = None              # this has to be changed
        self.summary_description = None     # has to be set to a fixed string


# end.
