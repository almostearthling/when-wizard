# file: share/when-wizard/modules/power-hibernate.py
# -*- coding: utf-8 -*-
#
# Task plugin to enter hibernation
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This action hibernates your Workstation, saving its current state and entering
a very low-consumption mode: depending on your OS release and your settings
the system will resume operations by either providing input or pressing the
power button. In some cases network activity could cause a wakeup.
"""


HIBERNATE_COMMAND = ""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_POWER,
            basename='power-hibernate',
            name='Hibernate',
            description='Hibernate your Workstation',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='download',
            help_string=HELP,
        )
        self.stock = True
        self.command_line = HIBERNATE_COMMAND


# end.
