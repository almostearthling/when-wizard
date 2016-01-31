# file: share/when-wizard/modules/misc-sendmail.py
# -*- coding: utf-8 -*-
#
# Task plugin to send an email
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
This task sends an e-mail message to the provided address. You can specify
the text (environment variables will be expanded if needed) and all the
parameters necessary to correctly perform the operation. This is useful if
you want to be notified of a certain event when you are away.
""")


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_MISC,
            basename='misc-sendmail',
            name=_("Email"),
            description=_("Send an E-mail Message"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='feedback',
            help_string=HELP,
        )
        self.stock = True


# end.
