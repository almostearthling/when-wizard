# file: share/when-wizard/templates/template-cond-command-plugin.py
# -*- coding: utf-8 -*-
#
# Template for a command based condition plugin
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


# uncomment the following line if localization is supported
import locale
from urllib.parse import urlparse
from plugin import CommandConditionPlugin, PLUGIN_CONST, plugin_name


# setup localization for both plugin text and configuration pane
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
Check whether or not the resource at the specified URL is available: if so
the condition will be verified and the associated consequence will fire up.
""")


cmd_template = """wget --spider -qO '%s'"""


class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Resource URL"),
            description=_("The Resource at the given URL is available"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='globe',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.category = PLUGIN_CONST.CATEGORY_COND_NETWORK
        self.resources.append('plugin_cond-net-urlavailable.glade')
        self.builder = self.get_dialog('plugin_cond-net-urlavailable')
        self.plugin_panel = None
        self.forward_allowed = False        # forward not enabled by default
        self.command_line = None            # full command line to run
        self.summary_description = None     # must be set for all plugins

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        url = o('txtEntry').get_text()
        if url:
            try:
                r = urlparse(url)
                if not r:
                    raise ValueError
                host = r.netloc.split(':')[0]
                self.summary_description = _("When a resource at '%s' is available") % host
                self.allow_forward(True)
                self.command_line = cmd_template % r.geturl()
            except Exception:
                self.summary_description = None
                self.command_line = None
                self.allow_forward(False)
        else:
            self.summary_description = None
            self.command_line = None
            self.allow_forward(False)


# end.
