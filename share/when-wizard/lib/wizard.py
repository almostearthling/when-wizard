# file: share/when-wizard/lib/wizard.py
# -*- coding: utf-8 -*-
#
# Implement the Wizard interface
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import time

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Pango

from utility import app_dialog_from_name, app_pixbuf_from_name

from resources import *
from plugin import PLUGIN_CONST
from plugin import stock_plugins_names, user_plugins_names, load_plugin_module
from plugin import store_plugin, store_association, add_to_file

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
    'finish',
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
        self.pane_Summary = self.get_view_Summary()
        self.pane_Finish = self.get_view_Finish()

        self.step_index = 0
        self.current_pane = None
        self.plugin_task = None
        self.plugin_cond = None
        self.enable_next = False
        self.enable_prev = True
        self.change_pane()
        self.refresh_buttons()

        # configuration
        self.direct_register = False        # directly register to When

    def get_view_TaskSel(self):
        p = self.builder_panes.get_object
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        store.append([app_pixbuf_from_name('process'),
                      PLUGIN_CONST.CATEGORY_TASK_APPS,
                      RESOURCES.UI_COMBO_CATEGORY_APPLICATIONS])
        store.append([app_pixbuf_from_name('settings'),
                      PLUGIN_CONST.CATEGORY_TASK_SETTINGS,
                      RESOURCES.UI_COMBO_CATEGORY_SETTINGS])
        store.append([app_pixbuf_from_name('key'),
                      PLUGIN_CONST.CATEGORY_TASK_SESSION,
                      RESOURCES.UI_COMBO_CATEGORY_SESSION])
        store.append([app_pixbuf_from_name('electricity'),
                      PLUGIN_CONST.CATEGORY_TASK_POWER,
                      RESOURCES.UI_COMBO_CATEGORY_POWER])
        store.append([app_pixbuf_from_name('folder'),
                      PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
                      RESOURCES.UI_COMBO_CATEGORY_FILEOPS])
        store.append([app_pixbuf_from_name('mind_map'),
                      PLUGIN_CONST.CATEGORY_TASK_MISC,
                      RESOURCES.UI_COMBO_CATEGORY_MISC])
        r_text = Gtk.CellRendererText()
        r_text_e = Gtk.CellRendererText()
        r_text_e.set_property("ellipsize", Pango.EllipsizeMode.MIDDLE)
        r_pixbuf = Gtk.CellRendererPixbuf()
        cb = p('cbCategory')
        cb.pack_start(r_text, True)
        cb.add_attribute(r_text, 'text', 2)
        cb.pack_start(r_pixbuf, False)
        cb.add_attribute(r_pixbuf, 'pixbuf', 0)
        cb.set_model(store)
        l = p('listActions')
        column_icon = Gtk.TreeViewColumn("Icon", r_pixbuf, pixbuf=1)
        column_name = Gtk.TreeViewColumn("Name", r_text, text=2)
        column_desc = Gtk.TreeViewColumn("Description", r_text_e, text=3)
        l.append_column(column_icon)
        l.append_column(column_name)
        l.append_column(column_desc)
        return p('viewTaskSel')

    def get_view_CondSel(self):
        p = self.builder_panes.get_object
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        store.append([app_pixbuf_from_name('clock'),
                      PLUGIN_CONST.CATEGORY_COND_TIME,
                      RESOURCES.UI_COMBO_CATEGORY_COND_TIME])
        store.append([app_pixbuf_from_name('clapperboard'),
                      PLUGIN_CONST.CATEGORY_COND_EVENT,
                      RESOURCES.UI_COMBO_CATEGORY_COND_EVENT])
        store.append([app_pixbuf_from_name('mind_map'),
                      PLUGIN_CONST.CATEGORY_COND_MISC,
                      RESOURCES.UI_COMBO_CATEGORY_COND_MISC])
        r_text = Gtk.CellRendererText()
        r_text_e = Gtk.CellRendererText()
        r_text_e.set_property("ellipsize", Pango.EllipsizeMode.MIDDLE)
        r_pixbuf = Gtk.CellRendererPixbuf()
        cb = p('cbCondType')
        cb.pack_start(r_text, True)
        cb.add_attribute(r_text, 'text', 2)
        cb.pack_start(r_pixbuf, False)
        cb.add_attribute(r_pixbuf, 'pixbuf', 0)
        cb.set_model(store)
        l = p('listConditions')
        column_icon = Gtk.TreeViewColumn("Icon", r_pixbuf, pixbuf=1)
        column_name = Gtk.TreeViewColumn("Name", r_text, text=2)
        column_desc = Gtk.TreeViewColumn("Description", r_text_e, text=3)
        l.append_column(column_icon)
        l.append_column(column_name)
        l.append_column(column_desc)
        return p('viewCondSel')

    def get_view_Summary(self):
        p = self.builder_panes.get_object
        r_text = Gtk.CellRendererText()
        r_text_e = Gtk.CellRendererText()
        r_text_e.set_property("ellipsize", Pango.EllipsizeMode.MIDDLE)
        r_pixbuf = Gtk.CellRendererPixbuf()
        column_icon = Gtk.TreeViewColumn("Icon", r_pixbuf, pixbuf=0)
        column_name = Gtk.TreeViewColumn("Item", r_text, text=1)
        column_desc = Gtk.TreeViewColumn("Description", r_text_e, text=2)
        l = p('listSummary')
        l.append_column(column_icon)
        l.append_column(column_name)
        l.append_column(column_desc)
        return p('viewSummary')

    def get_view_Finish(self):
        p = self.builder_panes.get_object
        return p('viewFinish')

    def show_about(self, *data):
        self.dialog_about.present()
        self.dialog_about.run()
        self.dialog_about.hide()

    def refresh_buttons(self):
        o = self.builder.get_object
        btn_next = o('btnForward')
        btn_prev = o('btnBack')
        if self.step_index > 0 and self.enable_prev:
            btn_prev.set_sensitive(True)
        else:
            btn_prev.set_sensitive(False)
        if self.step_index < len(WIZARD_STEPS) and self.enable_next:
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
            self.refresh_Summary()
            self.set_pane(self.pane_Summary)
        elif step == 'finish':
            self.set_pane(self.pane_Finish)

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
            all_plugins[m].plugin_type == PLUGIN_CONST.PLUGIN_TYPE_TASK)
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
        self.enable_next = False
        self.refresh_buttons()

    def changed_cbCondType(self, cb):
        p = self.builder_panes.get_object
        v = cb.get_active()
        model = cb.get_model()
        category = model[v][1]
        store = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str, str)
        related_plugins = (
            m for m in all_plugins if
            all_plugins[m].category == category and
            all_plugins[m].plugin_type == PLUGIN_CONST.PLUGIN_TYPE_CONDITION)
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
        self.enable_next = False
        self.refresh_buttons()

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
            self.enable_next = True
            self.refresh_buttons()
        else:
            t.set_text('')
            self.plugin_task = None
            self.pane_TaskDef = None
            self.enable_next = False
            self.refresh_buttons()

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
            self.enable_next = True
            self.refresh_buttons()
        else:
            t.set_text('')
            self.plugin_cond = None
            self.pane_CondDef = None
            self.enable_next = False
            self.refresh_buttons()

    def refresh_Summary(self):
        p = self.builder_panes.get_object
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        description = self.plugin_cond.summary_description()
        if description:
            store.append([app_pixbuf_from_name(self.plugin_cond.icon),
                          RESOURCES.UI_SUMMARY_CONDITION, description])
        description = self.plugin_task.summary_description()
        if description:
            store.append([app_pixbuf_from_name(self.plugin_task.icon),
                          RESOURCES.UI_SUMMARY_CONSEQUENCE, description])
        l = p('listSummary')
        l.set_model(store)

    def click_Next(self, o):
        if WIZARD_STEPS[self.step_index] == 'finish':
            self.dialog.hide()
            Gtk.main_quit()
        elif WIZARD_STEPS[self.step_index] == 'summary':
            self.plugin_cond.set_task(self.plugin_task.unique_id)
            self.register_action()
            self.step_index += 1
            self.change_pane()
            self.refresh_buttons()
        elif self.step_index < len(WIZARD_STEPS) - 1:
            self.step_index += 1
            self.change_pane()
            self.refresh_buttons()

    def click_Previous(self, o):
        if WIZARD_STEPS[self.step_index] == 'finish':
            self.step_index = 0
            self.change_pane()
            refresh_buttons()
        elif self.step_index > 0:
            self.step_index -= 1
            self.change_pane()
            self.refresh_buttons()

    # register action to the system
    def register_action(self):
        # TODO: this has to be replaced with more generic code, maybe
        #       it has to be included in specific functions for both
        #       plugin data registration and datastore operations
        if self.direct_register:
            task_item_dict = self.plugin_task.to_itemdef_dict()
            cond_item_dict = self.plugin_cond.to_itemdef_dict()
            # register to running isinstance
            print(task_item_dict)
            print(cond_item_dict)
        else:
            t = time.localtime()
            l = (self.plugin_task.basename, self.plugin_cond.basename)
            filename = time.strftime(RESOURCES.IDF_FILENAME_FORMAT, t)
            with open(filename, 'w') as f:
                f.write(RESOURCES.IDF_PREAMBLE_START %
                        time.strftime(RESOURCES.FORMAT_TIMESTAMP, t))
                f.write(RESOURCES.IDF_PREAMBLE_EXPLAIN_TASK %
                        self.plugin_task.summary_description())
                f.write(RESOURCES.IDF_PREAMBLE_EXPLAIN_CONDITION %
                        self.plugin_cond.summary_description())
                f.write(RESOURCES.IDF_PREAMBLE_EXPLAIN_PLUGINS % ", ".join(l))
                f.write(RESOURCES.IDF_PREAMBLE_END % filename)
                add_to_file(self.plugin_cond, f)
                add_to_file(self.plugin_task, f)
                f.write(RESOURCES.IDF_FOOTER)
        store_plugin(self.plugin_cond)
        store_plugin(self.plugin_task)
        store_association(self.plugin_cond, self.plugin_task)

    # wizard window main function
    def run(self):
        self.dialog.present()
        ret = self.dialog.run()
        self.dialog.hide()
        return ret


# The main application loader
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
