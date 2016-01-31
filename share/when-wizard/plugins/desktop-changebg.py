# file: share/when-wizard/modules/desktop-changebg.py
# -*- coding: utf-8 -*-
#
# Task plugin to change desktop background
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
Change the desktop background to the image you decide. Of course you can
switch it back to the original one using the desktop settings: this can be
useful to provide a strong alert when some event occurs.
""")


CHANGEBG_COMMAND = ""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_SETTINGS,
            basename='desktop-changebg',
            name=_("Change Background"),
            description=_("Modify the Desktop Background"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='gallery',
            help_string=HELP,
        )
        self.stock = True
        self.background_image = None
        self.command_line = ''


# end.
