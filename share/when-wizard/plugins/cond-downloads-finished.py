# file: share/when-wizard/modules/cond-downloads-finished.py
# -*- coding: utf-8 -*-
#
# Condition plugin that checks whether downloads have finished or not
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import locale
from plugin import CommandConditionPlugin, PLUGIN_CONST, plugin_name


# setup i18n for both applet text and dialogs
locale.setlocale(locale.LC_ALL, locale.getlocale())
locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
locale.textdomain(APP_NAME)
_ = locale.gettext


HELP = _("""\
This condition tests if files with extensions that indicate partial downloads
disappear from the main downloads directory: in other words, it fires when all
downloads have finished.
""")


class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Downloads Finished"),
            description=_("Check that all Active Downloads have Finished"),
            author=APP_AUTHOR,
            copyright=APP_COPYRIGHT,
            icon='business',
            help_string=HELP,
            version=APP_VERSION,
        )
        self.stock = True
        self.category = PLUGIN_CONST.CATEGORY_COND_FILESYSTEM
        self.script = self.get_script('plugin_cond-downloads-finished.sh')
        self.download_dir = "~/Downloads"
        self.command_line = '%s "%s"' % (self.script, self.download_dir)
        self.summary_description = _(
            "When all downloads in '%s' are complete") % self.download_dir


# end.
