# file: share/when-wizard/lib/wizard.py
# -*- coding: utf-8 -*-
#
# Implement the Wizard interface
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import time
import subprocess

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Pango

from utility import app_dialog, load_pixbuf

from resources import *
from plugin import PLUGIN_CONST, stock_plugins_names, user_plugins_names, \
    load_plugin_module, add_to_file, store_plugin, store_association, \
    register_plugin_data, unregister_plugin_data

_WIZARD_LOADER = 'when-wizard'
_WIZARD_WIZARD_SUBCOMMAND = 'start-wizard'
_WIZARD_MANAGER_SUBCOMMAND = 'start-manager'
_WIZARD_WIZARD_ICON = 'alarmclock_wand-128'
_WIZARD_MANAGER_ICON = 'alarmclock_wand-128'
_WIZARD_WIZARD_DLGICON = 'alarmclock_wand'
_WIZARD_MANAGER_DLGICON = 'alarmclock_wand'

# NOTE: all APP_... constants are builtins from the main script

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
ui_app_wizard_master = app_dialog('app-wizard-master')
ui_app_wizard_panes = app_dialog('app-wizard-panes')


# wizard steps
_WIZARD_STEPS = [
    'task_sel',
    'task_def',
    'cond_sel',
    'cond_def',
    'summary',
    'finish',
]


# the main wizard window
class WizardAppWindow(object):

    def __init__(self):
        self.builder = Gtk.Builder().new_from_string(ui_app_wizard_master, -1)
        self.builder.connect_signals(self)
        self.builder.set_translation_domain(APP_NAME)
        self.builder_panes = Gtk.Builder().new_from_string(
            ui_app_wizard_panes, -1)
        self.builder_panes.connect_signals(self)
        self.builder_panes.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        p = self.builder_panes.get_object
        self.dialog = o('dlgWhenWizardMaster')
        icon = load_pixbuf(_WIZARD_WIZARD_ICON)
        o('imgDeco').set_from_file(
            os.path.join(APP_GRAPHICS_FOLDER, 'wizard-side.png'))
        self.dialog.set_icon(icon)

        self.dialog_about = o('dlgAbout')
        self.dialog_about.set_icon(icon)
        self.dialog_about.set_logo(load_pixbuf(_WIZARD_WIZARD_ICON))
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
        self.pane_TaskDef_changed = False
        self.pane_CondDef_changed = False
        self.pane_CondSel_selected = False

        self.btntext_prev = o('btnBack').get_label()
        self.btntext_next = o('btnForward').get_label()

        self.step_index = 0
        self.current_pane = None
        self.plugin_task = None
        self.plugin_cond = None
        self.enable_next = False
        self.enable_prev = True
        self.register_error = False
        self.change_pane()
        self.refresh_buttons()

        # configuration
        self.direct_register = True

    def get_view_TaskSel(self):
        p = self.builder_panes.get_object
        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        store.append([load_pixbuf('process'),
                      PLUGIN_CONST.CATEGORY_TASK_APPS,
                      RESOURCES.UI_COMBO_CATEGORY_APPLICATIONS])
        store.append([load_pixbuf('settings'),
                      PLUGIN_CONST.CATEGORY_TASK_SETTINGS,
                      RESOURCES.UI_COMBO_CATEGORY_SETTINGS])
        store.append([load_pixbuf('key'),
                      PLUGIN_CONST.CATEGORY_TASK_SESSION,
                      RESOURCES.UI_COMBO_CATEGORY_SESSION])
        store.append([load_pixbuf('electricity'),
                      PLUGIN_CONST.CATEGORY_TASK_POWER,
                      RESOURCES.UI_COMBO_CATEGORY_POWER])
        store.append([load_pixbuf('folder'),
                      PLUGIN_CONST.CATEGORY_TASK_FILEOPS,
                      RESOURCES.UI_COMBO_CATEGORY_FILEOPS])
        store.append([load_pixbuf('mind_map'),
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
        store.append([load_pixbuf('clock'),
                      PLUGIN_CONST.CATEGORY_COND_TIME,
                      RESOURCES.UI_COMBO_CATEGORY_COND_TIME])
        store.append([load_pixbuf('folder'),
                      PLUGIN_CONST.CATEGORY_COND_FILESYSTEM,
                      RESOURCES.UI_COMBO_CATEGORY_COND_FILESYSTEM])
        store.append([load_pixbuf('clapperboard'),
                      PLUGIN_CONST.CATEGORY_COND_EVENT,
                      RESOURCES.UI_COMBO_CATEGORY_COND_EVENT])
        store.append([load_pixbuf('mind_map'),
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
        step = _WIZARD_STEPS[self.step_index]
        if step == 'finish':
            btn_next.set_label(RESOURCES.UI_BUTTON_FINISH)
            btn_prev.set_label(RESOURCES.UI_BUTTON_RESTART)
        else:
            btn_next.set_label(self.btntext_next)
            btn_prev.set_label(self.btntext_prev)
        if self.step_index > 0 and self.enable_prev:
            btn_prev.set_sensitive(True)
        else:
            btn_prev.set_sensitive(False)
        if self.step_index < len(_WIZARD_STEPS) and self.enable_next:
            if step == 'task_def' and self.pane_TaskDef_changed:
                btn_next.set_sensitive(self.plugin_task.forward_allowed)
            elif step == 'cond_def' and self.pane_CondDef_changed:
                btn_next.set_sensitive(self.plugin_cond.forward_allowed)
            elif step == 'cond_sel' and not self.pane_CondSel_selected:
                btn_next.set_sensitive(False)
            else:
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

    # simpler plugins have no config pane: in such cases pane is skipped
    def change_pane(self, forward=True):
        step = _WIZARD_STEPS[self.step_index]
        if step == 'task_sel':
            self.set_pane(self.pane_TaskSel)
        elif step == 'task_def':
            pane = self.pane_TaskDef
            if pane is not None:
                self.set_pane(pane)
            else:
                if forward:
                    self.step_index += 1
                    self.set_pane(self.pane_CondSel)
                else:
                    self.step_index -= 1
                    self.set_pane(self.pane_TaskSel)
        elif step == 'cond_sel':
            self.set_pane(self.pane_CondSel)
        elif step == 'cond_def':
            pane = self.pane_CondDef
            if pane is not None:
                self.set_pane(pane)
            else:
                if forward:
                    self.step_index += 1
                    self.refresh_Summary()
                    self.set_pane(self.pane_Summary)
                else:
                    self.step_index -= 1
                    self.set_pane(self.pane_CondSel)
        elif step == 'summary':
            self.refresh_Summary()
            self.set_pane(self.pane_Summary)
        elif step == 'finish':
            if self.register_error:
                self.builder_panes.get_object(
                    'lblFinish').set_text(RESOURCES.UI_FINISH_OPERATION_FAIL)
            else:
                self.builder_panes.get_object(
                    'lblFinish').set_text(RESOURCES.UI_FINISH_OPERATION_OK)
            self.set_pane(self.pane_Finish)
            self.register_error = False

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
            if all_plugins[m].enabled:
                elem = [
                    all_plugins[m].basename,
                    load_pixbuf(all_plugins[m].icon),
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
            if all_plugins[m].enabled:
                elem = [
                    all_plugins[m].basename,
                    load_pixbuf(all_plugins[m].icon),
                    all_plugins[m].name,
                    all_plugins[m].description,
                ]
                store.append(elem)
        l = p('listConditions')
        l.set_model(store)
        self.pane_CondSel_selected = True
        self.enable_next = False    # register action to the system
        self.refresh_buttons()

    def changed_listActions(self, sel):
        o = self.builder.get_object
        p = self.builder_panes.get_object
        m, i = sel.get_selected()
        t = p('txtHint').get_buffer()
        self.plugin_task_changed = True
        if i is not None:
            item = m[i][0]
            item_plugin = all_plugins[item]
            t.set_text(item_plugin.desc_string_gui())
            self.plugin_task = item_plugin
            self.plugin_task.set_forward_button(o('btnForward'))
            self.pane_TaskDef = item_plugin.get_pane()
            self.pane_TaskDef_changed = True
            self.enable_next = True
            self.refresh_buttons()
        else:
            t.set_text('')
            self.plugin_task = None
            self.pane_TaskDef = None
            self.enable_next = False
            self.refresh_buttons()

    def changed_listConditions(self, sel):
        o = self.builder.get_object
        p = self.builder_panes.get_object
        m, i = sel.get_selected()
        t = p('txtCondHint').get_buffer()
        self.plugin_cond_changed = True
        self.pane_CondDef_changed = True
        if i is not None:
            item = m[i][0]
            item_plugin = all_plugins[item]
            t.set_text(item_plugin.desc_string_gui())
            self.plugin_cond = item_plugin
            self.plugin_cond.set_forward_button(o('btnForward'))
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
        description = self.plugin_cond.summary_description
        if description:
            store.append([load_pixbuf(self.plugin_cond.icon),
                          RESOURCES.UI_SUMMARY_CONDITION, description])
        description = self.plugin_task.summary_description
        if description:
            store.append([load_pixbuf(self.plugin_task.icon),
                          RESOURCES.UI_SUMMARY_CONSEQUENCE, description])
        l = p('listSummary')
        l.set_model(store)

    def click_Next(self, obj):
        if _WIZARD_STEPS[self.step_index] == 'finish':
            self.dialog.hide()
            Gtk.main_quit()
        elif _WIZARD_STEPS[self.step_index] == 'summary':
            self.plugin_cond.set_task(self.plugin_task.unique_id)
            self.register_error = not self.register_action()
            self.step_index += 1
            self.change_pane(forward=True)
            self.refresh_buttons()
        elif self.step_index < len(_WIZARD_STEPS) - 1:
            self.step_index += 1
            self.change_pane(forward=True)
            self.refresh_buttons()

    def click_Previous(self, obj):
        if _WIZARD_STEPS[self.step_index] == 'finish':
            self.step_index = 0
            self.change_pane(forward=False)
            self.refresh_buttons()
        elif self.step_index > 0:
            self.step_index -= 1
            self.change_pane(forward=False)
            self.refresh_buttons()

    def register_action(self):
        if self.direct_register:
            # register to running instance
            if not register_plugin_data(self.plugin_task):
                return False
            if not register_plugin_data(self.plugin_cond):
                unregister_plugin_data(self.plugin_task)
                return False
        else:
            t = time.localtime()
            l = (self.plugin_task.basename, self.plugin_cond.basename)
            filename = time.strftime(RESOURCES.IDF_FILENAME_FORMAT, t)
            filepath = os.path.join(USER_STORE_FOLDER, filename)
            with open(filepath, 'w') as f:
                f.write(RESOURCES.IDF_PREAMBLE_START %
                        time.strftime(RESOURCES.FORMAT_TIMESTAMP, t))
                f.write(RESOURCES.IDF_PREAMBLE_EXPLAIN_TASK %
                        self.plugin_task.summary_description)
                f.write(RESOURCES.IDF_PREAMBLE_EXPLAIN_CONDITION %
                        self.plugin_cond.summary_description)
                f.write(RESOURCES.IDF_PREAMBLE_EXPLAIN_PLUGINS % ", ".join(l))
                f.write(RESOURCES.IDF_PREAMBLE_END % filename)
                add_to_file(self.plugin_cond, f)
                add_to_file(self.plugin_task, f)
                f.write(RESOURCES.IDF_FOOTER)
            try:
                ret = subprocess.call('%s --item-add %s' % (APP_WHEN, filepath),
                                      shell=True)
                if ret != 0:
                    return False
            except OSError:
                return False
        store_plugin(self.plugin_cond)
        store_plugin(self.plugin_task)
        store_association(self.plugin_cond, self.plugin_task)
        return True

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

    def app_activate(self, app_instance):
        self.main()

    def main(self):
        main_window = WizardAppWindow()
        return main_window.run()


# end.
