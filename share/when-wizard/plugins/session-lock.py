# file: share/when-wizard/modules/session-lock.py
# -*- coding: utf-8 -*-
#
# Task plugin to lock the session
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This task locks your session without logging you out: it protects your
Workstation by asking for a password to start over to work, but does not
close any application.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_SESSION,
            basename='session-lock',
            name='Lock',
            description='Session Lock',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='lock',
            help_string=HELP,
        )
        self.stock = True


# end.
