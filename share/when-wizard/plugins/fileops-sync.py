# file: share/when-wizard/modules/fileops-sync.py
# -*- coding: utf-8 -*-
#
# Task plugin to synchronize directories
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import locale
from plugin import TaskPlugin, PLUGIN_CONST, plugin_name

from gi.repository import Gtk

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This action synchronizes two directories: it copies all files in the source
directory to the destination making sure that files in both directories are
always up to date. It can also propagate deletions if desired. This is useful
for unattended backups of valuable data.
""")


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename=plugin_name(__file__),
            name=_("Synchronize"),
            description=_("Synchronize Two Directories"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='advance',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.script = self.get_script('plugin_fileops-sync.sh')
        self.builder = self.get_dialog('plugin_fileops-sync')
        self.plugin_panel = None
        self.forward_allowed = False
        self.source = None
        self.destination = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def click_btnSource(self, obj):
        o = self.builder.get_object
        dlg = Gtk.FileChooserDialog(
            _("Choose source directory"), None,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        if filename:
            o('txtSource').set_text(filename)

    def click_btnDestination(self, obj):
        o = self.builder.get_object
        dlg = Gtk.FileChooserDialog(
            _("Choose destination directory"), None,
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

    def change_paths(self, obj):
        o = self.builder.get_object
        source = o('txtSource').get_text()
        destination = o('txtDestination').get_text()
        self.command_line = None
        self.summary_description = None
        if os.path.isdir(source) and os.path.isdir(destination):
            sourcename = os.path.basename(source)
            destname = os.path.basename(destination)
            self.source = source
            self.destination = destination
            self.command_line = '%s %s %s' % (
                self.script, self.source, self.destination)
            self.summary_description = _(
                "Files from %s will be copied to %s") % (sourcename, destname)
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
