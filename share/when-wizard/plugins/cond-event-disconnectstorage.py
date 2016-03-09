# file: share/when-wizard/templates/cond-event-disconnectstorage.py
# -*- coding: utf-8 -*-
#
# Condition plugin for external storage disconnection
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will be fired when an external storage device is detached from the
workstation: no detail is given about the storage device, the associated
consequence should take care of discovering what is no more available.
""")


EVENT_SYSTEM_DEVICE_DETACH = 'device_detach'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Disconnect Storage"),
            description=_("An External Storage Device is Disconnected"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='delete_database',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_FILESYSTEM
        self.stock = True
        self.event = EVENT_SYSTEM_DEVICE_DETACH
        self.summary_description = _(
            "When a storage device is detached from the computer")


# end.
