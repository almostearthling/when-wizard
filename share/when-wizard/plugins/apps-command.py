# file: share/when-wizard/modules/apps-command.py
# -*- coding: utf-8 -*-
#
# Task plugin to start a command
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This task is used to start a non-interactive system command: you can provide
the whole command line that will be executed in the background without user
interaction.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_APPS,
            basename='apps-command',
            name='Command Launcher',
            description='Start a System Command',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='start',
            help_string=HELP,
        )
        self.stock = True


# end.
