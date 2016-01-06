# file: share/when-wizard/modules/wizard.py
# -*- coding: utf-8 -*-
#
# Implement the Wizard interface
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import os.path

from gi.repository import GLib, Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

from dialogs import load_app_dialog

# NOTE: all APP_... constants are builtins from the main script


ui_app_wizard_master = load_app_dialog('app-wizard-master')


class WizardAppWindow(object):

    def __init__(self):
        self.builder = Gtk.Builder().new_from_string(ui_app_wizard_master, -1)
        self.builder.connect_signals(self)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.dialog = o('dlgWhenWizardMaster')
        # image = o('imgDeco')
        # image.new_from_file(os.path.join(APP_GRAPHICS_FOLDER,
        #                                  'wizard-side.png'))
        image = o('imgDeco')
        image.set_from_file(os.path.join(APP_GRAPHICS_FOLDER,
                                         'wizard-side.png'))
        # print(os.path.join(APP_GRAPHICS_FOLDER, 'wizard-side.png'))
        # image = Gtk.Image.new_from_file(os.path.join(APP_GRAPHICS_FOLDER,
        #                                              'wizard-side.png'))
        # o('imgDeco').new_from_pixbuf(image.get_pixbuf())


    def run(self):
        self.dialog.set_keep_above(True)
        self.dialog.present()
        ret = self.dialog.run()
        self.dialog.hide()
        self.dialog.set_keep_above(False)
        return ret


class WizardApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id=APP_ID,
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.register(None)
        self.connect('activate', self.app_activate)

    def app_activate(self, applet_instance):
        self.main()

    def main(self):
        main_window = WizardAppWindow()
        return main_window.run()


# end.
