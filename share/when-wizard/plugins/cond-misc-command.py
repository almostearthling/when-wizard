# file: share/when-wizard/templates/cond-misc-command.py
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import CommandConditionPlugin, PLUGIN_CONST

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This tests a command by periodically running it in the background, and if
it succeeds (that is, it has an exit status of zero) the associated task
is run as a consequence. It can also run specially crafted scripts so that
virtually everything in the system can be checked.
""")


# class for a plugin: the derived class name should always be Plugin
class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename='cond-misc-command',
            name=_("Command"),
            description=_("Check successful execution of command"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='start',
            help_string=HELP,
        )
        # the items below might be not needed and can be deleted if the
        # plugin does not have a configuration panel
        self.stock = True
        self.builder = self.get_dialog('plugin_cond-misc-command')
        self.plugin_panel = None

        # mandatory or anyway structural variables and object values follow:
        self.command_line = None            # full command line to run
        self.summary_description = None     # must be set for all plugins

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    # all following methods are optional

    def change_entry(self, obj):
        o = self.builder.get_object
        self.command_line = o('txtCommand').get_text()
        if value:
            command_name = os.path.basename(self.command_line.split()[0])
            self.summary_description = _(
                "A command based on '%s' will be run") % command_name
        else:
            self.command_line = None
            self.summary_description = None


# end.
