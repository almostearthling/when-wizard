# file: share/when-wizard/modules/fileops-openfile.py
# -*- coding: utf-8 -*-
#
# Task plugin to open a file
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This task opens a file in its associated default application: it uses the
system settings to determine the action to perform (that is, the application
used) to open the specified file. The file can be read and, if you have the
permissions, modified and saved interactively.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-openfile',
            name='Open File',
            description='Open a File',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='file',
            help_string=HELP,
        )
        self.stock = True


# end.
