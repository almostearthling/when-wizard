# file: share/when-wizard/modules/wizard.py
# -*- coding: utf-8 -*-
#
# Implement the Wizard interface
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import os.path

from gi.repository import GLib, Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Pango

from utility import app_dialog_from_name
from utility import app_pixbuf_from_name

from resources import RESOURCES as R
from plugin import CONST as P
from plugin import stock_plugins_names, user_plugins_names, load_plugin_module

# NOTE: all APP_... constants are builtins from the main script

# mockup for the overall interface test
# from plugins_mockup import PLUGINS as all_plugins
# load all plugins
all_plugins = {}
for name in stock_plugins_names():
    m = load_plugin_module(name, stock=True)
    if m:
        all_plugins[name] = m.Plugin()
for name in user_plugins_names():
    m = load_plugin_module(name)
    if m:
        all_plugins[name] = m.Plugin()


# load windows and stock panes
ui_app_wizard_master = app_dialog_from_name('app-wizard-master')
ui_app_wizard_panes = app_dialog_from_name('app-wizard-panes')


# wizard steps
WIZARD_STEPS = [
    'task_sel',
    'task_def',
    'cond_sel',
    'cond_def',
    'summary',
]


class WizardAppWindow(object):

    def __init__(self):
        self.builder = Gtk.Builder().new_from_string(ui_app_wizard_master, -1)
        self.builder.connect_signals(self)
        self.builder.set_translation_domain(APP_NAME)
        self.builder_panes = Gtk.Builder().new_from_string(ui_app_wizard_panes, -1)
        self.builder_panes.connect_signals(self)
        self.builder_panes.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        p = self.builder_panes.get_object
        self.dialog = o('dlgWhenWizardMaster')
        self.icon = Gtk.Image.new_from_file(
            os.path.join(APP_GRAPHICS_FOLDER, 'alarmclock_wand.png'))
        self.logo = Gtk.Image.new_from_file(
            os.path.join(APP_GRAPHICS_FOLDER, 'alarmclock_wand-128.png'))
        o('imgDeco').set_from_file(os.path.join(APP_GRAPHICS_FOLDER,
                                                'wizard-side.png'))
        self.dialog.set_icon(self.icon.get_pixbuf())

        self.dialog_about = o('dlgAbout')
        self.dialog_about.set_icon(self.icon.get_pixbuf())
        self.dialog_about.set_logo(self.logo.get_pixbuf())
        self.dialog_about.set_program_name(APP_SHORTNAME)
        self.dialog_about.set_website(APP_URL)
        self.dialog_about.set_copyright(APP_COPYRIGHT)
        self.dialog_about.set_comments(APP_LONGDESC)
        self.dialog_about.set_version(APP_VERSION)

        self.pane_TaskSel = self.get_view_TaskSel()
        self.pane_TaskDef = None
        self.pane_CondSel = self.get_view_CondSel()
        self.pane_CondDef = None
        self.pane_Summary = None

        self.step_index = 0
        self.current_pane = None
        self.plugin_task = None
        self.plugin_cond = None
        self.change_pane()

    def get_view_TaskSel(self):
        p = self.builder_panes.get_object
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        store.append([app_pixbuf_from_name('process'), P.CATEGORY_TASK_APPS,
                      R.UI_COMBO_CATEGORY_APPLICATIONS])
        store.append([app_pixbuf_from_name('settings'),
                      P.CATEGORY_TASK_SETTINGS,
                      R.UI_COMBO_CATEGORY_SETTINGS])
        store.append([app_pixbuf_from_name('key'), P.CATEGORY_TASK_SESSION,
                      R.UI_COMBO_CATEGORY_SESSION])
        store.append([app_pixbuf_from_name('electricity'),
                      P.CATEGORY_TASK_POWER,
                      R.UI_COMBO_CATEGORY_POWER])
        store.append([app_pixbuf_from_name('folder'), P.CATEGORY_TASK_FILEOPS,
                      R.UI_COMBO_CATEGORY_FILEOPS])
        store.append([app_pixbuf_from_name('mind_map'), P.CATEGORY_TASK_MISC,
                      R.UI_COMBO_CATEGORY_MISC])
        r_text = Gtk.CellRendererText()
        r_pixbuf = Gtk.CellRendererPixbuf()
        cb = p('cbCategory')
        cb.pack_start(r_text, True)
        cb.add_attribute(r_text, 'text', 2)
        cb.pack_start(r_pixbuf, False)
        cb.add_attribute(r_pixbuf, 'pixbuf', 0)
        cb.set_model(store)
        l = p('listActions')
        # column_id = Gtk.TreeViewColumn("ID", r_text, text=0)
        column_icon = Gtk.TreeViewColumn("Icon", r_pixbuf, pixbuf=1)
        column_name = Gtk.TreeViewColumn("Name", r_text, text=2)
        column_desc = Gtk.TreeViewColumn("Description", r_text, text=3)
        # l.append_column(column_id)
        l.append_column(column_icon)
        l.append_column(column_name)
        l.append_column(column_desc)
        return p('viewTaskSel')

    def get_view_CondSel(self):
        p = self.builder_panes.get_object
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        store.append([app_pixbuf_from_name('clock'), P.CATEGORY_COND_TIME,
                      R.UI_COMBO_CATEGORY_COND_TIME])
        store.append([app_pixbuf_from_name('clapperboard'), P.CATEGORY_COND_EVENT,
                      R.UI_COMBO_CATEGORY_COND_EVENT])
        store.append([app_pixbuf_from_name('mind_map'), P.CATEGORY_COND_MISC,
                      R.UI_COMBO_CATEGORY_COND_MISC])
        r_text = Gtk.CellRendererText()
        r_pixbuf = Gtk.CellRendererPixbuf()
        cb = p('cbCondType')
        cb.pack_start(r_text, True)
        cb.add_attribute(r_text, 'text', 2)
        cb.pack_start(r_pixbuf, False)
        cb.add_attribute(r_pixbuf, 'pixbuf', 0)
        cb.set_model(store)
        l = p('listConditions')
        # column_id = Gtk.TreeViewColumn("ID", r_text, text=0)
        column_icon = Gtk.TreeViewColumn("Icon", r_pixbuf, pixbuf=1)
        column_name = Gtk.TreeViewColumn("Name", r_text, text=2)
        column_desc = Gtk.TreeViewColumn("Description", r_text, text=3)
        # l.append_column(column_id)
        l.append_column(column_icon)
        l.append_column(column_name)
        l.append_column(column_desc)
        return p('viewCondSel')

    def show_about(self, *data):
        self.dialog_about.present()
        self.dialog_about.run()
        self.dialog_about.hide()

    def refresh_buttons(self):
        o = self.builder.get_object
        btn_next = o('btnForward')
        btn_prev = o('btnBack')
        if self.step_index > 0:
            btn_prev.set_sensitive(True)
        else:
            btn_prev.set_sensitive(False)
        if self.step_index < len(WIZARD_STEPS) - 1:
            btn_next.set_sensitive(True)
        else:
            btn_next.set_sensitive(False)

    def set_pane(self, pane):
        o = self.builder.get_object
        if self.current_pane is not None:
            o('paneWizard').remove(self.current_pane)
        if pane is not None:
            o('paneWizard').add(pane)
        self.current_pane = pane

    def change_pane(self):
        step = WIZARD_STEPS[self.step_index]
        if step == 'task_sel':
            self.set_pane(self.pane_TaskSel)
        elif step == 'task_def':
            self.set_pane(self.pane_TaskDef)
        elif step == 'cond_sel':
            self.set_pane(self.pane_CondSel)
        elif step == 'cond_def':
            self.set_pane(self.pane_CondDef)
        elif step == 'summary':
            self.set_pane(self.pane_Summary)

    # control reactions
    def changed_cbCategory(self, cb):
        p = self.builder_panes.get_object
        v = cb.get_active()
        model = cb.get_model()
        category = model[v][1]
        store = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str, str)
        related_plugins = (
            m for m in all_plugins if
            all_plugins[m].category == category and
            all_plugins[m].plugin_type == P.PLUGIN_TYPE_TASK)
        sorted_plugins = [(all_plugins[m].name, m) for m in related_plugins]
        sorted_plugins.sort()
        for x in sorted_plugins:
            m = x[1]
            elem = [
                all_plugins[m].basename,
                app_pixbuf_from_name(all_plugins[m].icon),
                all_plugins[m].name,
                all_plugins[m].description,
            ]
            store.append(elem)
        l = p('listActions')
        l.set_model(store)

    def changed_cbCondType(self, cb):
        p = self.builder_panes.get_object
        v = cb.get_active()
        model = cb.get_model()
        category = model[v][1]
        store = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str, str)
        related_plugins = (
            m for m in all_plugins if
            all_plugins[m].category == category and
            all_plugins[m].plugin_type == P.PLUGIN_TYPE_CONDITION)
        sorted_plugins = [(all_plugins[m].name, m) for m in related_plugins]
        sorted_plugins.sort()
        for x in sorted_plugins:
            m = x[1]
            elem = [
                all_plugins[m].basename,
                app_pixbuf_from_name(all_plugins[m].icon),
                all_plugins[m].name,
                all_plugins[m].description,
            ]
            store.append(elem)
        l = p('listConditions')
        l.set_model(store)

    def changed_listActions(self, sel):
        p = self.builder_panes.get_object
        m, i = sel.get_selected()
        t = p('txtHint').get_buffer()
        if i is not None:
            item = m[i][0]
            item_plugin = all_plugins[item]
            t.set_text(item_plugin.desc_string_gui())
            self.plugin_task = item_plugin
            self.pane_TaskDef = item_plugin.get_pane()
        else:
            t.set_text('')
            self.plugin_task = None
            self.pane_TaskDef = None

    def changed_listConditions(self, sel):
        p = self.builder_panes.get_object
        m, i = sel.get_selected()
        t = p('txtCondHint').get_buffer()
        if i is not None:
            item = m[i][0]
            item_plugin = all_plugins[item]
            t.set_text(item_plugin.desc_string_gui())
            self.plugin_cond = item_plugin
            self.pane_CondDef = item_plugin.get_pane()
        else:
            t.set_text('')
            self.plugin_cond = None
            self.pane_CondDef = None

    def click_Next(self, o):
        if self.step_index < len(WIZARD_STEPS) - 1:
            self.step_index += 1
            self.change_pane()
            self.refresh_buttons()

    def click_Previous(self, o):
        if self.step_index > 0:
            self.step_index -= 1
            self.change_pane()
            self.refresh_buttons()

    # wizard window main function
    def run(self):
        self.dialog.present()
        ret = self.dialog.run()
        self.dialog.hide()
        return ret


class WizardApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id=APP_ID,
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.register(None)
        self.connect('activate', self.app_activate)

    def app_activate(self, applet_instance):
        self.main()

    def main(self):
        main_window = WizardAppWindow()
        return main_window.run()


# end.
