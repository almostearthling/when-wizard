# file: share/when-wizard/modules/fileops-mediacopy.py
# -*- coding: utf-8 -*-
#
# Task plugin to synchronize directories
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
Use this task to copy files from a certain removable storage device (such as
an USB stick or a CD-ROM) to a selected destination directory. The removable
storage device is recognized by its label, which has to be specified.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-mediacopy',
            name='Media Copy',
            description='Copy from Removable Media',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='briefcase',
            help_string=HELP,
        )
        self.stock = True


# end.
