# file: share/when-wizard/modules/misc-sound.py
# -*- coding: utf-8 -*-
#
# Task plugin to play a sound
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
This actions plays the specified sound when the chosen condition occurs:
it can be useful if you are near the computer and you want audible feedback
about a certain event.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_MISC,
            basename='misc-sound',
            name=_("Sound"),
            description=_("Play a Sound"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='speaker',
            help_string=HELP,
        )
        self.stock = True


# end.
