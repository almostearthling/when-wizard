# file: share/when-wizard/modules/fileops-mediacopy.py
# -*- coding: utf-8 -*-
#
# Task plugin to synchronize directories
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
Use this task to copy files from a certain removable storage device (such as
an USB stick or a CD-ROM) to a selected destination directory. The removable
storage device is recognized by its label, which has to be specified.
""")


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-mediacopy',
            name=_("Media Copy"),
            description=_("Copy from Removable Media"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='briefcase',
            help_string=HELP,
        )
        self.stock = True
        self.script = self.get_script('plugin_fileops-mediacopy.sh')
        self.builder = self.get_dialog('plugin_fileops-mediacopy')
        self.plugin_panel = None
        self.media_label = None
        self.destination = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def click_btnDestination(self, obj):
        o = self.builder.get_object
        dlg = Gtk.FileChooserDialog(
            _("Choose a directory"), None,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        if filename:
            o('txtDestination').set_text(filename)

    def click_btnRefresh(self, obj):
        o = self.builder.get_object
        # TODO: ...

    def change_paths(self, obj):
        o = self.builder.get_object
        media_label = o('txtMediaLabel').get_text()
        destination = o('txtDestination').get_text()
        self.command_line = None
        self.summary_description = None
        if os.path.isdir(destination):
            destname = os.path.basename(destination)
            self.media_label = media_label
            self.destination = destination
            if self.media_label:
                self.command_line = '%s %s %s' % (
                    self.script, self.media_label, self.destination)
                self.summary_description = _(
                    "Files from %s will be copied to %s") % (
                    self.media_label, destname)


# end.
