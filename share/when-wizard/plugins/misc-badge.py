# file: share/when-wizard/modules/misc-badge.py
# -*- coding: utf-8 -*-
#
# Task plugin to show a notification badge
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This actions shows a notification badge when the chosen condition occurs:
it can be useful if you are at the computer and you want visible feedback
about a certain event.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_MISC,
            basename='misc-badge',
            name='Show Badge',
            description='Show a Notification Badge',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='sms',
            help_string=HELP,
        )
        self.stock = True


# end.
