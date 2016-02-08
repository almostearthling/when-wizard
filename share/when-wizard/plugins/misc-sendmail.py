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

cmd_template = '{script} "{mailto}" "{title}" "{message}"'


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
            version="0.1~alpha.0",
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_misc-sendmail')
        self.plugin_panel = None
        self.forward_allowed = False
        self.message = None
        self.title = None
        self.mailto = None

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        message = o('txtMessage').get_text()
        title = o('txtTitle').get_text()
        mailto = o('txtMailTo').get_text()
        if message and title and mailto:
            self.message = message
            self.title = title
            self.command_line = cmd_template.format(
                script=self.get_script('plugin_misc-sendmail.sh'),
                title=title, message=message, mailto=mailto)
            self.summary_description = _(
                "An email will be sent to %s") % mailto
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
