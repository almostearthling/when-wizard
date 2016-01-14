# file: share/when-wizard/modules/fileops-openfile.py
# -*- coding: utf-8 -*-
#
# Task plugin to show a directory
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This task opens a directory in the default file manager application. The
specified directory is shown on your desktop and you can search for files
and perform any file operations as long as permissions are granted to do so.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-openfile',
            name='Open Directory',
            description='Show a Directory',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='folder',
            help_string=HELP,
        )
        self.stock = True


# end.
