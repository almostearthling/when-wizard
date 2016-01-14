# file: share/when-wizard/modules/desktop-changebg.py
# -*- coding: utf-8 -*-
#
# Task plugin to change desktop background
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
Change the desktop background to the image you decide. Of course you can
switch it back to the original one using the desktop settings: this can be
useful to provide a strong alert when some event occurs.
"""


CHANGEBG_COMMAND = ""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_SETTINGS,
            basename='desktop-changebg',
            name='Change Background',
            description='Modify the Desktop Background',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='gallery',
            help_string=HELP,
        )
        self.stock = True
        self.background_image = None
        self.command_line = ''


# end.
