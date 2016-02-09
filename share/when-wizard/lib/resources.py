# file: share/when-wizard/lib/resources.py
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

    # Non-UI related resources
    FORMAT_TIMESTAMP = '%Y-%m-%d %H:%M:%S'

    IDF_PREAMBLE_START = "# Item definition file created on %s\n"
    IDF_PREAMBLE_EXPLAIN_CONDITION = "# Action condition: %s\n"
    IDF_PREAMBLE_EXPLAIN_TASK = "# Action task: %s\n"
    IDF_PREAMBLE_EXPLAIN_PLUGINS = "# Plugins: %s\n"
    IDF_PREAMBLE_END = "# Import this file using 'when-command --item-add %s'\n\n"
    IDF_COMMENT = "# %s"
    IDF_FOOTER = "# end.\n"
    IDF_FILENAME_FORMAT = 'itemdefs-%Y%m%d_%H%M%S.when'

    # command line messages
    CLI_ERR_NOTFOUND_WHEN = _("could not find a running instance of When")

    # ComboBox entries
    UI_COMBO_CATEGORY_APPLICATIONS = _("Applications")
    UI_COMBO_CATEGORY_SETTINGS = _("Desktop and System Settings")
    UI_COMBO_CATEGORY_SESSION = _("Session Management")
    UI_COMBO_CATEGORY_POWER = _("Power Management")
    UI_COMBO_CATEGORY_FILEOPS = _("File and Folder Operations")
    UI_COMBO_CATEGORY_MISC = _("Miscellaneous")

    UI_COMBO_CATEGORY_COND_TIME = _("Time Related")
    UI_COMBO_CATEGORY_COND_EVENT = _("Session or System Event")
    UI_COMBO_CATEGORY_COND_MISC = _("Miscellaneous")

    # Fill summary list with meaningful entries
    UI_SUMMARY_CONDITION = _("Condition:")
    UI_SUMMARY_CONSEQUENCE = _("Consequence:")

    # Messages for when the wizard finishes
    UI_FINISH_OPERATION_OK = _("The action was correctly registered!")
    UI_FINISH_OPERATION_FAIL = _("The action could not be registered: please try again.")

    # Button text
    UI_BUTTON_FINISH = _("Finish")
    UI_BUTTON_RESTART = _("Restart")


# a single instance of the class will contain all resource strings
RESOURCES = Resources()


# end.
