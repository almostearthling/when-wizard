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
    IDF_FILENAME_FORMAT = 'itemdefs-%Y%m%d_%H%M%S.widf'

    # desktop entry constants
    DESKTOP_ENTRY_WIZARD_NAME = "When Wizard"
    DESKTOP_ENTRY_WIZARD_COMMENT = _("When Wizard: Main Wizard Application")
    DESKTOP_ENTRY_MANAGER_NAME = "When Wizard Manager"
    DESKTOP_ENTRY_MANAGER_COMMENT = _("When Wizard: Manager Utility")

    # command line interface messages
    CLI_ERR_NOTFOUND_WHEN = _("could not find a running instance of When")
    CLI_ERR_INVALID_ARGUMENTS = _("required arguments missing or invalid")
    CLI_ERR_FAIL_INSTALL_PLUGIN = _("the specified plugin could not be installed")
    CLI_ERR_FAIL_UNINSTALL_PLUGIN = _("the specified plugin could not be uninstalled")
    CLI_ERR_FAIL_PACKAGE_PLUGIN = _("could not package plugin: check file names")
    CLI_ERR_FAIL_LOAD_PLUGIN = _("the required plugin could not be loaded")
    CLI_ERR_FAIL_RUN_PLUGIN = _("the required plugin could not be loaded")

    CLI_MSG_PLUGIN_PACKAGED = _("plugin successfully packaged")
    CLI_MSG_PLUGINS_PACKAGED = _("%s plugins successfully packaged")

    # file filter specifications
    FILTER_PLUGIN_PACKAGE_NAME = "Plugin Package"
    FILTER_PLUGIN_PACKAGE_PATTERN = '*.wwpz'
    FILTER_IDF_NAME = "Item Definition"
    FILTER_IDF_PATTERN = '*.widf'
    FILTER_IDF_EXTENSION = '.widf'

    # ComboBox entries
    UI_COMBO_CATEGORY_APPLICATIONS = _("Applications")
    UI_COMBO_CATEGORY_SETTINGS = _("Desktop and System Settings")
    UI_COMBO_CATEGORY_SESSION = _("Session Management")
    UI_COMBO_CATEGORY_POWER = _("Power Management")
    UI_COMBO_CATEGORY_FILEOPS = _("File and Folder Operations")
    UI_COMBO_CATEGORY_MISC = _("Miscellaneous")

    UI_COMBO_CATEGORY_COND_TIME = _("Time Related")
    UI_COMBO_CATEGORY_COND_FILESYSTEM = _("Files and Directories")
    UI_COMBO_CATEGORY_COND_EVENT = _("Session or System Event")
    UI_COMBO_CATEGORY_COND_MISC = _("Miscellaneous")

    # column headers
    UI_COLUMN_HEAD_CONDITION = _("Condition")
    UI_COLUMN_HEAD_TASK = _("Consequence")
    # UI_COLUMN_HEAD_ICON = _("Icon")
    UI_COLUMN_HEAD_ICON = ""
    UI_COLUMN_HEAD_TIME = _("Time")
    UI_COLUMN_HEAD_NAME = _("Name")
    UI_COLUMN_HEAD_DESCRIPTION = _("Description")
    UI_COLUMN_HEAD_DURATION = _("Duration")
    UI_COLUMN_HEAD_OUTCOME = _("Success")

    # Fill summary list with meaningful entries
    UI_SUMMARY_CONDITION = _("Condition:")
    UI_SUMMARY_CONSEQUENCE = _("Consequence:")

    # Messages for when the wizard finishes
    UI_FINISH_OPERATION_OK = _("The action was correctly registered!")
    UI_FINISH_OPERATION_FAIL = _("The action could not be registered: please try again.")

    # Button text
    UI_BUTTON_FINISH = _("Finish")
    UI_BUTTON_RESTART = _("Restart")

    # message boxes
    MSGBOX_CONFIRM_DELETE_ASSOCIATION = _("Are you sure you want to delete the selected action?")
    MSGBOX_CONFIRM_DELETE_ALL_ASSOCIATIONS = _("Are you sure you want to delete all actions?")
    MSGBOX_CONFIRM_UNINSTALL_PLUGIN = _("Are you sure you want to uninstall the %s plugin?")
    MSGBOX_CONFIRM_UNIMPORT_ITEMS = _("Are you sure you want to remove items imported from %s?")

    MSGBOX_ERR_INSTALL_PLUGIN = _("The specified plugin could not be installed.\nEnsure that it is a proper package and/or contact the author.")
    MSGBOX_ERR_UNINSTALL_PLUGIN = _("The specified plugin could not be uninstalled.")
    MSGBOX_OK_INSTALL_PLUGIN = _("The plugin has been correctly installed.")
    MSGBOX_OK_UNINSTALL_PLUGIN = _("The plugin has been correctly uninstalled.")
    MSGBOX_ERR_IMPORT_IDF = _("The specified item definition file could\nnot be imported. Check file consistency.")
    MSGBOX_ERR_IMPORT_IDF_READ = _("The item definition file could not be read.")
    MSGBOX_ERR_IMPORT_IDF_EXISTS = _("An item definition file with the same name\nhas been already imported: remove it first.")
    MSGBOX_ERR_UNIMPORT_IDF = _("Not all items from the specified definition file\ncould be removed: please check dependencies.")
    MSGBOX_OK_IMPORT_IDF = _("Items imported successfully.")
    MSGBOX_OK_UNIMPORT_IDF = _("Items removed successfully.")
    MSGBOX_ERR_DBUS_COMMUNICATION = _("Unable to communicate with a running When instance.")
    MSGBOX_ERR_DBUS_APPLYCHANGES = _("Could not apply at least part of the requested changes.")
    MSGBOX_ERR_DESKTOP_ICONS = _("Could not create all desktop icons.")
    MSGBOX_OK_APPLYCHANGES = _("All changes applied successfully.")

    # dialog box text and titles
    UI_TITLE_CHOOSE_PACKAGE_FILE = _("Choose a Package File")
    UI_TITLE_CHOOSE_IDF_FILE = _("Choose an Item Definition File")

# a single instance of the class will contain all resource strings
RESOURCES = Resources()


# end.
