# file: share/when-wizard/modules/misc-badge.py
# -*- coding: utf-8 -*-
#
# Task plugin to show a notification badge
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import locale
from plugin import TaskPlugin, PLUGIN_CONST

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from utility import load_pixbuf

# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This action shows a notification badge when the chosen condition occurs:
it can be useful if you are at the computer and you want visible feedback
about a certain event.
""")


cmd_template = 'notify-send {icon_spec} "{title}" "{message}"'


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_MISC,
            basename='misc-badge',
            name=_("Show Badge"),
            description=_("Show a Notification Badge"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='sms',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.builder = self.get_dialog('plugin_misc-badge')
        self.plugin_panel = None
        self.forward_allowed = False
        self.message = None
        self.title = None
        self.iconname = None
        self.summary_description = _("A notification badge will be displayed")

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            r_text = Gtk.CellRendererText()
            r_pixbuf = Gtk.CellRendererPixbuf()
            store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
            store.append([load_pixbuf('info'),
                          _("Information"), 'dialog-information'])
            store.append([load_pixbuf('questions'),
                          _("Question"), 'dialog-question'])
            store.append([load_pixbuf('high_priority'),
                          _("Warning"), 'dialog-warning'])
            store.append([load_pixbuf('cancel'),
                          _("Error"), 'dialog-error'])
            cb = o('cbIcon')
            cb.pack_start(r_text, True)
            cb.add_attribute(r_text, 'text', 1)
            cb.pack_start(r_pixbuf, False)
            cb.add_attribute(r_pixbuf, 'pixbuf', 0)
            cb.set_model(store)
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_icon(self, obj):
        i = obj.get_active_iter()
        if i is not None:
            m = obj.get_model()
            self.iconname = m[i][2]
        else:
            self.iconname = None

    def change_entry(self, obj):
        o = self.builder.get_object
        message = o('txtBadgeMessage').get_text()
        title = o('txtBadgeTitle').get_text()
        if message and title:
            self.message = message
            self.title = title
            if self.iconname:
                icon_spec = '-i %s' % self.iconname
            else:
                icon_spec = ''
            self.command_line = cmd_template.format(
                icon_spec=icon_spec, title=title, message=message)
            self.allow_forward(True)
        else:
            self.command_line = None
            self.allow_forward(False)


# end.
