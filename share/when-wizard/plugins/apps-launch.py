# file: share/when-wizard/modules/apps-launch.py
# -*- coding: utf-8 -*-
#
# Task plugin to launch an application
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


from plugin import TaskPlugin, CONST


HELP = """\
Use this action to launch a desktop application: choose one from the list
and it will be started once the referring condition occurs. You will be
able to interact with the application and will have to close it yourself
when you finished using it.
"""


# the name should always be Plugin
class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            category=CONST.CATEGORY_TASK_APPS,
            basename='apps-launch',
            name='Application Launcher',
            description='apps-launch',
            author='Francesco Garosi',
            copyright='Copyright (c) 2016',
            icon='electro_devices',
            help_string=HELP,
        )
        self.stock = True
        self.module_basename = 'apps-launch'
        self.module_path = None




# end.
