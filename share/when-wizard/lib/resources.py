# file: share/when-wizard/modules/dialogs.py
# -*- coding: utf-8 -*-
#
# Resources and constants
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

# NOTE: all APP_... constants are builtins from the main script

import os
import sys
import locale


# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


# action constants
ACTION_OK = 0
ACTION_CANCEL = -1
ACTION_DELETE = 9

# user interface constants
UI_INTERVALS_MINUTES = [1, 2, 3, 5, 15, 30, 60]
UI_INTERVALS_HOURS = [1, 2, 3, 4, 6, 8, 12, 24]


class Resources(object):

    # Step 1: Deal With ComboBox entries
    UI_COMBO_CATEGORY_APPLICATIONS = _("Applications")
    UI_COMBO_CATEGORY_SETTINGS = _("Desktop and System Settings")
    UI_COMBO_CATEGORY_SESSION = _("Session Management")
    UI_COMBO_CATEGORY_POWER = _("Power Management")
    UI_COMBO_CATEGORY_FILEOPS = _("File and Folder Operations")
    UI_COMBO_CATEGORY_MISC = _("Miscellaneous")


# a single instance of the class will contain all resource strings
RESOURCES = Resources()


# end.
