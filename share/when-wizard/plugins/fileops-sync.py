# file: share/when-wizard/modules/fileops-sync.py
# -*- coding: utf-8 -*-
#
# Task plugin to synchronize directories
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
This action synchronizes two directories: it copies all files in the source
directory to the destination making sure that files in both directories are
always up to date. It can also propagate deletions if desired. This is useful
for unattended backups of valuable data.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=CONST.CATEGORY_TASK_FILEOPS,
            basename='fileops-sync',
            name='Synchronize',
            description='Synchronize Two Directories',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='advance',
            help_string=HELP,
        )
        self.stock = True


# end.
