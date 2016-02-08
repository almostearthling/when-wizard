# file: share/when-wizard/plugins/misc-sound.py
# -*- coding: utf-8 -*-
#
# Task plugin to play a sound
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
This actions plays the specified sound when the chosen condition occurs:
it can be useful if you are near the computer and you want audible feedback
about a certain event.
""")


cmd_template = 'xdg-open "%s"'


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_MISC,
            basename='misc-sound',
            name=_("Sound"),
            description=_("Play a Sound"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='speaker',
            help_string=HELP,
            version="0.1~alpha.0",
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_misc-sound')
        self.plugin_panel = None
        self.path = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def click_btnChoose(self, obj):
        o = self.builder.get_object
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Sound files")
        filter_img.add_mime_type("audio/wav")
        filter_img.add_mime_type("audio/mpeg")
        filter_img.add_mime_type("audio/aac")
        filter_img.add_mime_type("audio/mp4")
        filter_img.add_mime_type("audio/ogg")
        dlg = Gtk.FileChooserDialog(
            _("Choose a file"), None,
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
            self.path = os.path.realpath(path)
            self.command_line = cmd_template % self.path
            self.summary_description = _(
                "The sound '%s' will be played") % name
        else:
            self.path = None
            self.command_line = None
            self.summary_description = None


# end.
