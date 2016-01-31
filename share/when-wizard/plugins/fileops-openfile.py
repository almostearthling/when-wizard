# file: share/when-wizard/modules/fileops-openfile.py
# -*- coding: utf-8 -*-
#
# Task plugin to open a file
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import TaskPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This task opens a file in its associated default application: it uses the
system settings to determine the action to perform (that is, the application
used) to open the specified file. The file can be read and, if you have the
permissions, modified and saved interactively.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-openfile',
            name=_("Open File"),
            description=_("Open a File"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='file',
            help_string=HELP,
        )
        self.stock = True


# end.
