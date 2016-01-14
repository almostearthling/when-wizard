# file: share/when-wizard/modules/misc-sound.py
# -*- coding: utf-8 -*-
#
# Task plugin to play a sound
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This actions plays the specified sound when the chosen condition occurs:
it can be useful if you are near the computer and you want audible feedback
about a certain event.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_MISC,
            basename='misc-sound',
            name='Sound',
            description='Play a Sound',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='speaker',
            help_string=HELP,
        )
        self.stock = True


# end.
