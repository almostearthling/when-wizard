# file: share/when-wizard/modules/plugins_mockup.py
# -*- coding: utf-8 -*-
#
# Mockup module containing fake plugin definitions for testing purposes
# Copyright (c) 2015-2016
# Released under the BSD License (see LICENSE file)


from app_plugin import ApplicationPlugin, PLUGIN_CONSTANTS


# the list of all (mock) plugins
PLUGINS = {
    'applications-launch': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='apps',
        basename='applications-launch',
        name='Application Launcher',
        description='Launch a Desktop Application',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='electro_devices',
        helpstring='Use this task to launch an application that will interact with you through its graphical user interface.',
        default=True,
    ),
    'applications-cmdexec': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='apps',
        basename='applications-cmdexec',
        name='Command Launcher',
        description='Run a System Command',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='electronics',
        helpstring='Use this task to run a system command. The action will be performed and the outcome can possibly be checked.',
        default=True,
    ),
    'settings-background': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='settings',
        basename='settings-background',
        name='Set Background',
        description='Change your Desktop Background Image',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='gallery',
        helpstring='This task changes your desktop background to the image that you specify.',
        default=True,
    ),
    'settings-spam': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='settings',
        basename='settings-spam',
        name='Spam Egg',
        description='Viking-Like Egg Spammer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='workflow',
        helpstring='This action can be used to spam your egg until it frobnicates all the way round.',
        default=True,
    ),
    'settings-parrot': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='settings',
        basename='settings-parrot',
        name='Blue Parrot',
        description='Unfortunately Dead Parrot',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='entering_heaven_alive',
        helpstring='You stunned him, just as he was waking up! Norwegian Blues stun easily, major.',
        default=True,
    ),
    'fileops-open': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='fileops',
        basename='fileops-open',
        name='Open File',
        description='Open a File',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='file',
        helpstring='This task opens a file with its associated desktop application and shows it.',
        default=True,
    ),
    'fileops-opendir': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='fileops',
        basename='fileops-opendir',
        name='Open Folder',
        description='Open a Directory',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='folder',
        helpstring='This task can be used to open a directory using the default desktop file manager.',
        default=True,
    ),
    'power-shutdown': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='power',
        basename='power-shutdown',
        name='Shutdown',
        description='Shut Down your Computer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='no_idea',
        helpstring='Use this action to shutdown your personal computer gracefully.',
        default=True,
    ),
    'power-reboot': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='power',
        basename='power-reboot',
        name='Reboot',
        description='Reboot your Computer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='synchronize',
        helpstring='Use this action to reboot your personal computer.',
        default=True,
    ),
    'power-hibernate': ApplicationPlugin(
        plugintype=PLUGIN_CONSTANTS.PLUGIN_TYPE_TASK,
        category='power',
        basename='power-hibernate',
        name='Hibernate',
        description='Suspend your Computer',
        author='Francesco Garosi',
        copyright='Copyright (c) 2016',
        icon='download',
        helpstring='Use this action to suspend your personal computer to a very low-power state to be able to resume later.',
        default=True,
    ),

}


# end.
