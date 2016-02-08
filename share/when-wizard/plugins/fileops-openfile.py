# file: share/when-wizard/modules/fileops-openfile.py
# -*- coding: utf-8 -*-
#
# Task plugin to open a file
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import locale
from plugin import TaskPlugin, PLUGIN_CONST

from gi.repository import Gtk

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This task opens a file in its associated default application: it uses the
system settings to determine the action to perform (that is, the application
used) to open the specified file. The file can be read and, if you have the
permissions, modified and saved interactively.
""")


cmd_template = 'xdg-open "%s"'


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-openfile',
            name=_("Open File"),
            description=_("Open a File"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='file',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_fileops-openfile')
        self.plugin_panel = None
        self.forward_allowed = False
        self.path = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def click_btnChoose(self, obj):
        o = self.builder.get_object
        dlg = Gtk.FileChooserDialog(
            _("Choose a file"), None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        if filename:
            o('txtFilename').set_text(filename)

    def change_filename(self, obj):
        o = self.builder.get_object
        path = o('txtFilename').get_text()
        if path:
            name = os.path.basename(path)
            self.path = os.path.realpath(path)
            self.command_line = cmd_template % self.path
            self.summary_description = _(
                "The file '%s' will be open") % name
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
