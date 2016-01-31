# file: share/when-wizard/modules/fileops-mediacopy.py
# -*- coding: utf-8 -*-
#
# Task plugin to synchronize directories
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
Use this task to copy files from a certain removable storage device (such as
an USB stick or a CD-ROM) to a selected destination directory. The removable
storage device is recognized by its label, which has to be specified.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-mediacopy',
            name=_("Media Copy"),
            description=_("Copy from Removable Media"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='briefcase',
            help_string=HELP,
        )
        self.stock = True


# end.
