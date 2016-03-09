# file: share/when-wizard/plugins/cond-fs-dirchange.py
# -*- coding: utf-8 -*-
#
# Fire an event when a file changes
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import locale
from plugin import FileChangeConditionPlugin, PLUGIN_CONST, plugin_name
from gi.repository import Gtk


# setup localization for both plugin text and configuration pane
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This condition can be used to monitor all files in a directory: when any
changes occur recursively in any files within the chosen directory, the
event will fire up and trigger a consequence.
""")


class Plugin(FileChangeConditionPlugin):

    def __init__(self):
        FileChangeConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Directory Monitor"),
            description=_("Monitor a directory for changes"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='folder',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-fs-dirchange')
        self.plugin_panel = None
        self.forward_allowed = False        # forward not enabled by default
        self.watched_path = None            # file or directory to observe
        self.summary_description = None     # must be set for all plugins

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def click_btnBrowse(self, obj):
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
            o('txtFilename').set_text(filename)

    def change_filename(self, obj):
        o = self.builder.get_object
        self.watched_path = o('txtFilename').get_text()
        if self.watched_path:
            base = os.path.basename(self.watched_path)
            self.summary_description = _(
                "When files in directory '%s' change") % base
            self.allow_forward(True)
        else:
            self.watched_path = None
            self.summary_description = None
            self.allow_forward(False)


# end.
