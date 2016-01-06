# file: share/when-wizard/modules/dialogs.py
# -*- coding: utf-8 -*-
#
# Dialog boxes and windows utilities
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import sys

from gi.repository import GLib, Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

# NOTE: all APP_... constants are builtins from the main script


def load_app_dialog(name):
    base = os.path.dirname(sys.argv[0])
    with open(os.path.join(APP_RESOURCE_FOLDER, '%s.glade' % name)) as f:
        dialog_xml = f.read()
    return dialog_xml


# end.
