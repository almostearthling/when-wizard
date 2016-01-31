# file: share/when-wizard/modules/fileops-openfile.py
# -*- coding: utf-8 -*-
#
# Task plugin to show a directory
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
This task opens a directory in the default file manager application. The
specified directory is shown on your desktop and you can search for files
and perform any file operations as long as permissions are granted to do so.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-openfile',
            name=_("Open Directory"),
            description=_("Show a Directory in File Manager"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='folder',
            help_string=HELP,
        )
        self.stock = True


# end.
