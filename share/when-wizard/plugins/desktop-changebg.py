# file: share/when-wizard/modules/desktop-changebg.py
# -*- coding: utf-8 -*-
#
# Task plugin to change desktop background
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
Change the desktop background to the image you decide. Of course you can
switch it back to the original one using the desktop settings: this can be
useful to provide a strong alert when some event occurs.
""")


cmd_template = 'gsettings set org.gnome.desktop.background picture-uri "file://%s"'


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_SETTINGS,
            basename='desktop-changebg',
            name=_("Change Background"),
            description=_("Modify the Desktop Background"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='gallery',
            help_string=HELP,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_desktop-changebg')
        self.plugin_panel = None
        self.background_image = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def click_btnChoose(self, obj):
        o = self.builder.get_object
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Image files")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_mime_type("image/png")
        dlg = Gtk.FileChooserDialog(
            _("Choose an image file"), None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dlg.add_filter(filter_img)
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
            self.background_image = os.path.realpath(path)
            self.command_line = cmd_template % self.background_image
            self.summary_description = _(
                "Background image will be changed to '%s'") % name
        else:
            self.background_image = None
            self.command_line = None
            self.summary_description = None


# end.
