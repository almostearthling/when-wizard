# file: share/when-wizard/templates/cond-event-joinnetwork.py
# -*- coding: utf-8 -*-
#
# Condition plugin for network connection
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
This event will be fired when a network is joined: no detail is given about
the network, the associated consequence should take care of finding it out.
""")


EVENT_SYSTEM_NETWORK_JOIN = 'network_join'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Join Network"),
            description=_("A New Network Connection is Available"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='flash_on',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_NETWORK
        self.stock = True
        self.event = EVENT_SYSTEM_NETWORK_JOIN
        self.summary_description = _("When a new network connection is joined")


# end.
