# file: share/when-wizard/templates/cond-event-connectstorage.py
# -*- coding: utf-8 -*-
#
# Condition plugin for external storage connection
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will be fired when an external storage device is connected to the
workstation: no detail is given about the storage device, the associated
consequence should take care of discovering what is available.
""")


EVENT_SYSTEM_DEVICE_ATTACH = 'device_attach'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Connect Storage"),
            description=_("An External Storage Device is Connected"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='add_database',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_FILESYSTEM
        self.stock = True
        self.event = EVENT_SYSTEM_DEVICE_ATTACH
        self.summary_description = _("When a storage device is connected to the computer")


# end.
