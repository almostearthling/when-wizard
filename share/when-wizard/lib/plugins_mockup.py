# file: share/when-wizard/modules/plugins_mockup.py
# -*- coding: utf-8 -*-
#
# Mockup module containing fake plugin definitions for testing purposes
# Copyright (c) 2015-2016
# Released under the BSD License (see LICENSE file)


import plugin


# the list of all (mock) plugins
PLUGINS = {
    'applications-launch': plugin.TaskPlugin(
        category='apps',
        basename='applications-launch',
        name='Application Launcher',
        description='Launch a Desktop Application',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='electro_devices',
        help_string='Use this task to launch an application that will interact with you through its graphical user interface.',
    ),
    'applications-cmdexec': plugin.TaskPlugin(
        category='apps',
        basename='applications-cmdexec',
        name='Command Launcher',
        description='Run a System Command',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='electronics',
        help_string='Use this task to run a system command. The action will be performed and the outcome can possibly be checked.',
    ),
    'settings-background': plugin.TaskPlugin(
        category='settings',
        basename='settings-background',
        name='Set Background',
        description='Change your Desktop Background Image',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='gallery',
        help_string='This task changes your desktop background to the image that you specify.',
    ),
    'settings-spam': plugin.TaskPlugin(
        category='settings',
        basename='settings-spam',
        name='Spam Egg',
        description='Viking-Like Egg Spammer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='workflow',
        help_string='This action can be used to spam your egg until it frobnicates all the way round.',
    ),
    'settings-parrot': plugin.TaskPlugin(
        category='settings',
        basename='settings-parrot',
        name='Blue Parrot',
        description='Unfortunately Dead Parrot',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='entering_heaven_alive',
        help_string='You stunned him, just as he was waking up! Norwegian Blues stun easily, major.',
    ),
    'fileops-open': plugin.TaskPlugin(
        category='fileops',
        basename='fileops-open',
        name='Open File',
        description='Open a File',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='file',
        help_string='This task opens a file with its associated desktop application and shows it.',
    ),
    'fileops-opendir': plugin.TaskPlugin(
        category='fileops',
        basename='fileops-opendir',
        name='Open Folder',
        description='Open a Directory',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='folder',
        help_string='This task can be used to open a directory using the default desktop file manager.',
    ),
    'power-shutdown': plugin.TaskPlugin(
        category='power',
        basename='power-shutdown',
        name='Shutdown',
        description='Shut Down your Computer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='no_idea',
        help_string='Use this action to shutdown your personal computer gracefully.',
    ),
    'power-reboot': plugin.TaskPlugin(
        category='power',
        basename='power-reboot',
        name='Reboot',
        description='Reboot your Computer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='synchronize',
        help_string='Use this action to reboot your personal computer.',
    ),
    'power-hibernate': plugin.TaskPlugin(
        category='power',
        basename='power-hibernate',
        name='Hibernate',
        description='Suspend your Computer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='download',
        help_string='Use this action to suspend your personal computer to a very low-power state to be able to resume later.',
    ),

}


# end.
