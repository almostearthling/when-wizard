# file: share/when-wizard/templates/cond-event-cond-event-resume.py
# -*- coding: utf-8 -*-
#
# Condition plugin for the session resume event
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import EventConditionPlugin, PLUGIN_CONST, plugin_name

# Gtk might be needed: uncomment if this is the case
# from gi.repository import Gtk

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This event will occur when the session resumes from hibernation mode.
""")


EVENT_SYSTEM_RESUME = 'system_resume'


class Plugin(EventConditionPlugin):

    def __init__(self):
        EventConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Resume"),
            description=_("Exit the low consumption mode"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='mms',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.category = PLUGIN_CONST.CATEGORY_COND_POWER
        self.stock = True
        self.event = EVENT_SYSTEM_RESUME
        self.summary_description = _("When the session is resumed")


# end.
