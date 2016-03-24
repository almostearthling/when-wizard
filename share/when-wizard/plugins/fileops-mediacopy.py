# file: share/when-wizard/modules/fileops-mediacopy.py
# -*- coding: utf-8 -*-
#
# Task plugin to copy from storage media
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
Use this task to copy files from a certain removable storage device (such as
an USB stick) to a selected destination directory. The removable storage device
is recognized by its label, which has to be specified.
""")


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename=plugin_name(__file__),
            name=_("Media Copy"),
            description=_("Copy from Removable Media"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='briefcase',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_fileops-mediacopy')
        self.plugin_panel = None
        self.forward_allowed = False
        self.media_label = None
        self.destination = None
        self.data = self.data_retrieve()
        if self.data is None:
            self.data = {
                'device_labels': [],
            }
        self.device_labels = self.data['device_labels']

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
            cb = o('cbMediaLabel')
            cb.get_model().clear()
            for x in self.device_labels:
                cb.append_text(x)
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

    # find the attached USB device: a possible solution is here
    # http://askubuntu.com/a/168654/466738
    # however since we rely on the device label, a scan of /media/$USER
    # should be performed anyway; maybe that in case the system does not
    # automount devices it has to be GVFS-mounted too
    def click_btnRefresh(self, obj):
        o = self.builder.get_object
        cb = o('cbMediaLabel')
        cb.get_model().clear()
        dirs = (os.path.basename(x)
                for x in os.listdir('/media/%s' % os.environ['USER']))
        for x in dirs:
            if x not in self.device_labels:
                self.device_labels.append(x)
        self.device_labels.sort()
        self.data['device_labels'] = self.device_labels
        self.data_store(self.data)
        for x in self.device_labels:
            cb.append_text(x)

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
                    self.get_script('plugin_fileops-mediacopy.sh'),
                    self.media_label, self.destination)
                self.summary_description = _(
                    "Files from '%s' will be copied to '%s'") % (
                    self.media_label, destname)
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
