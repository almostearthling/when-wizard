# file: share/when-wizard/modules/apps-launch.py
# -*- coding: utf-8 -*-
#
# Task plugin to launch an application
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import locale
from plugin import TaskPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
Use this action to launch a desktop application: choose one from the list
and it will be started once the referring condition occurs. You will be
able to interact with the application and will have to close it yourself
when you finished using it.
""")


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_APPS,
            basename='apps-launch',
            name=_("Application Launcher"),
            description=_("Start an Application"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='electro_devices',
            help_string=HELP,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_apps-launch')
        self.plugin_panel = None
        self.app_name = None

    # see http://python-gtk-3-tutorial.readthedocs.org/en/latest/iconview.html
    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            o('appChooser').set_show_all(True)
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def select_application(self, obj, desktop_app):
        desktop_filename = desktop_app.get_filename()
        self.app_name = desktop_app.get_string("Name")
        self.command_line = '%s run-desktop %s' % (
            os.path.join(APP_BIN_FOLDER, 'when-wizard'), desktop_filename)
        self.summary_description = _(
            "The application '%s' will be started") % self.app_name
        self.allow_forward(True)


# end.
