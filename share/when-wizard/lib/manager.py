# file: share/when-wizard/lib/manager.py
# -*- coding: utf-8 -*-
#
# Implement the Wizard Manager application
# Copyright (c) 2015-2016 Francesco Garosi
# Released under the BSD License (see LICENSE file)

import os
import time
import dbus
import subprocess

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Pango

from utility import app_dialog, load_pixbuf, when_proxy, \
    when_apply_options, write_desktop_entry, \
    WHEN_OPTIONS_REACTIVITY_LAZY, WHEN_OPTIONS_REACTIVITY_NORMAL, \
    WHEN_OPTIONS_GENERIC

from itemimport import idf_exists, idf_install, idf_remove, \
    idf_installed_list, param_file, replace_params

from resources import *
from plugin import PLUGIN_CONST, stock_plugins_names, user_plugins_names, \
    load_plugin_module, unstore_association, unregister_plugin_data, \
    retrieve_action_history, retrieve_plugin_data, retrieve_plugin, \
    active_plugins_names, retrieve_association, retrieve_association_ids, \
    install_plugin, uninstall_plugin, \
    enable_association_id, retrieve_association_ids_suspended

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
ui_app_manager = app_dialog('app-manager')
ui_app_manager_paramidf = app_dialog('app-manager-paramidf')


# the main wizard manager window
class ManagerAppWindow(object):

    def __init__(self):
        self.builder = Gtk.Builder().new_from_string(ui_app_manager, -1)
        self.builder.connect_signals(self)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.dialog = o('dlgManager')
        icon = load_pixbuf(_WIZARD_MANAGER_DLGICON)
        self.glyph_success = load_pixbuf('success')
        self.glyph_failure = load_pixbuf('failure')
        self.glyph_enabled = load_pixbuf('enabled')
        self.glyph_disabled = load_pixbuf('disabled')
        self.dialog.set_icon(icon)

        self.dialog_about = o('dlgAbout')
        self.dialog_about.set_icon(icon)
        self.dialog_about.set_logo(load_pixbuf(_WIZARD_MANAGER_ICON))
        self.dialog_about.set_program_name(APP_SHORTNAME)
        self.dialog_about.set_website(APP_URL)
        self.dialog_about.set_copyright(APP_COPYRIGHT)
        self.dialog_about.set_comments(APP_LONGDESC)
        self.dialog_about.set_version(APP_VERSION)

        # dialog data
        self.selected_association = None
        self.selected_uninstallplugin = None
        self.selected_unimportidf = None
        self.install_package = None
        self.import_idf = None

        # default sensitivity and checked states
        o('btnDelete').set_sensitive(False)
        o('btnDeleteAll').set_sensitive(False)
        o('btnInstall').set_sensitive(False)
        o('btnUninstall').set_sensitive(False)
        o('btnImport').set_sensitive(False)
        o('btnUnimport').set_sensitive(False)
        if APP_BIN_FOLDER.startswith('/usr'):
            o('chkDesktopIcons').set_sensitive(False)

        # prepare controls
        r_text = Gtk.CellRendererText()
        r_text_e = Gtk.CellRendererText()
        r_text_e.set_property('ellipsize', Pango.EllipsizeMode.MIDDLE)
        r_pixbuf = Gtk.CellRendererPixbuf()
        column_cond_active = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=6)
        column_cond_icon = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=1)
        column_cond_name = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_CONDITION, r_text, text=2)
        column_cond_name.set_expand(True)
        column_arrow = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=3)
        column_task_icon = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=4)
        column_task_name = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_TASK, r_text, text=5)
        column_task_name.set_expand(True)
        l = o('listAssociation')
        l.append_column(column_cond_active)
        l.append_column(column_cond_icon)
        l.append_column(column_cond_name)
        l.append_column(column_arrow)
        l.append_column(column_task_icon)
        l.append_column(column_task_name)
        self.fill_listAssociations(None)

        column_cond_time = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_TIME, r_text, text=0)
        column_cond_icon = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=1)
        column_cond_name = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_CONDITION, r_text, text=2)
        column_cond_name.set_expand(True)
        column_arrow = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=3)
        column_task_icon = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_ICON, r_pixbuf, pixbuf=4)
        column_task_name = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_TASK, r_text, text=5)
        column_task_name.set_expand(True)
        column_outcome = Gtk.TreeViewColumn(
            RESOURCES.UI_COLUMN_HEAD_OUTCOME, r_pixbuf, pixbuf=6)
        l = o('listHistory')
        l.append_column(column_cond_time)
        l.append_column(column_cond_icon)
        l.append_column(column_cond_name)
        l.append_column(column_arrow)
        l.append_column(column_task_icon)
        l.append_column(column_task_name)
        l.append_column(column_outcome)
        self.fill_listHistory(None)

        cb = o('cbSelectUninstallPlugin')
        cb.pack_start(r_text, True)
        cb.add_attribute(r_text, 'text', 0)
        cb.pack_start(r_pixbuf, False)
        cb.add_attribute(r_pixbuf, 'pixbuf', 1)
        self.fill_cbSelectUninstallPlugin(None)

        cb = o('cbSelectUnimport')
        cb.pack_start(r_text, True)
        cb.add_attribute(r_text, 'text', 0)
        self.fill_cbSelectUnimport(None)

        # visible sections of multi-pane pages
        self.changed_action_rbInstall(None)
        self.changed_action_rbImport(None)

    def show_about(self, *data):
        self.dialog_about.present()
        self.dialog_about.run()
        self.dialog_about.hide()

    def fill_listAssociations(self, obj):
        o = self.builder.get_object
        store = Gtk.ListStore(str,
                              GdkPixbuf.Pixbuf, str,
                              GdkPixbuf.Pixbuf,
                              GdkPixbuf.Pixbuf, str,
                              GdkPixbuf.Pixbuf, bool)
        association_ids = retrieve_association_ids()
        suspended = retrieve_association_ids_suspended()
        arrow = load_pixbuf('right')
        l = o('listAssociation')
        delall_sensitive = False
        for x in association_ids:
            li = retrieve_association(x)
            cond_name = li[0]
            cond_active = bool(x not in suspended)
            cond_active_pixbuf = \
                self.glyph_enabled if cond_active else self.glyph_disabled
            cond_data = retrieve_plugin_data(cond_name)
            cond_pixbuf = load_pixbuf(cond_data['icon'])
            task_name = li[1]
            task_data = retrieve_plugin_data(task_name)
            task_pixbuf = load_pixbuf(task_data['icon'])
            store.append([x,
                          cond_pixbuf, cond_data['name'], arrow,
                          task_pixbuf, task_data['name'],
                          cond_active_pixbuf, cond_active])
            delall_sensitive = True
        l.set_model(store)
        o('btnDeleteAll').set_sensitive(delall_sensitive)

    def fill_listHistory(self, obj):
        o = self.builder.get_object
        h = retrieve_action_history()
        l = o('listHistory')
        store = Gtk.ListStore(str,
                              GdkPixbuf.Pixbuf, str,
                              GdkPixbuf.Pixbuf,
                              GdkPixbuf.Pixbuf, str,
                              GdkPixbuf.Pixbuf)
        arrow = load_pixbuf('right')
        for x in h:
            store.append([
                "%s (%.2fs)" % (x['datetime'].split()[1], x['duration']),
                x['cond_icon'],
                x['cond_name'],
                arrow,
                x['task_icon'],
                x['task_name'],
                self.glyph_success if x['success'] else self.glyph_failure,
            ])
        l.set_model(store)

    def fill_cbSelectUninstallPlugin(self, obj):
        o = self.builder.get_object
        store = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
        user_plugins = user_plugins_names()
        active_plugins = active_plugins_names()
        removable_plugins = []
        for x in user_plugins:
            if x not in active_plugins:
                removable_plugins.append(x)
        for x in removable_plugins:
            store.append([
                x,
                load_pixbuf(all_plugins[x].icon),
            ])
        o('cbSelectUninstallPlugin').set_model(store)
        self.selected_uninstallplugin = None

    def fill_cbSelectUnimport(self, obj):
        o = self.builder.get_object
        store = Gtk.ListStore(str)
        for idf in idf_installed_list():
            store.append([idf])
        o('cbSelectUnimport').set_model(store)
        self.selected_unimportidf = None

    def changed_listAssociation(self, sel):
        o = self.builder.get_object
        m, i = sel.get_selected()
        if i is not None:
            self.selected_association = m[i][0]
            enabled = m[i][7]
            li = retrieve_association(self.selected_association)
            data_cond = retrieve_plugin_data(li[0])
            data_task = retrieve_plugin_data(li[1])
            o('txtCondition').set_text(data_cond['summary_description'])
            o('txtConsequence').set_text(data_task['summary_description'])
            o('btnDelete').set_sensitive(True)
            if enabled:
                o('btnEnable').set_sensitive(False)
                o('btnDisable').set_sensitive(True)
            else:
                o('btnEnable').set_sensitive(True)
                o('btnDisable').set_sensitive(False)
        else:
            o('txtCondition').set_text("")
            o('txtConsequence').set_text("")
            o('btnDelete').set_sensitive(False)
            o('btnEnable').set_sensitive(False)
            o('btnDisable').set_sensitive(False)

    def changed_cbSelectUninstallPlugin(self, cb):
        o = self.builder.get_object
        i = cb.get_active_iter()
        if i is not None:
            m = cb.get_model()
            self.selected_uninstallplugin = m[i][0]
            plugin = all_plugins[self.selected_uninstallplugin]
            o('txtUninstallPluginName').set_text(plugin.name)
            o('txtUninstallPluginDescription').set_text(plugin.description)
            o('btnUninstall').set_sensitive(True)
        else:
            self.selected_uninstallplugin = None
            o('txtUninstallPluginName').set_text("")
            o('txtUninstallPluginDescription').set_text("")
            o('btnUninstall').set_sensitive(False)

    def changed_cbSelectUnimport(self, cb):
        o = self.builder.get_object
        i = cb.get_active_iter()
        if i is not None:
            m = cb.get_model()
            self.selected_unimportidf = m[i][0]
            o('btnUnimport').set_sensitive(True)
        else:
            self.selected_uninstallplugin = None
            o('btnUnimport').set_sensitive(False)

    def changed_txtChoosePackage(self, obj):
        o = self.builder.get_object
        path = o('txtChoosePackage').get_text()
        if os.path.exists(path) and os.path.isfile(os.path.realpath(path)):
            self.install_package = path
            o('btnInstall').set_sensitive(True)
        else:
            self.install_package = None
            o('btnInstall').set_sensitive(False)

    def changed_txtChooseIDF(self, obj):
        o = self.builder.get_object
        path = o('txtChooseIDF').get_text()
        if os.path.exists(path) and os.path.isfile(os.path.realpath(path)):
            self.import_idf = path
            o('btnImport').set_sensitive(True)
        else:
            self.import_idf = None
            o('btnImport').set_sensitive(False)

    def click_btnDelete(self, obj):
        o = self.builder.get_object
        if self.selected_association:
            confirmbox = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                           buttons=Gtk.ButtonsType.YES_NO)
            confirmbox.set_markup(
                RESOURCES.MSGBOX_CONFIRM_DELETE_ASSOCIATION)
            ret = confirmbox.run()
            confirmbox.hide()
            confirmbox.destroy()
            if ret == Gtk.ResponseType.YES:
                li = retrieve_association(self.selected_association)
                plugin_cond = retrieve_plugin(li[0])
                plugin_task = retrieve_plugin(li[1])
                unregister_plugin_data(plugin_cond)
                unregister_plugin_data(plugin_task)
                unstore_association(self.selected_association)
                self.selected_association = None
                self.fill_listAssociations(None)
                self.fill_cbSelectUninstallPlugin(None)
                o('txtCondition').set_text("")
                o('txtConsequence').set_text("")

    def click_btnDeleteAll(self, obj):
        o = self.builder.get_object
        confirmbox = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                       buttons=Gtk.ButtonsType.YES_NO)
        confirmbox.set_markup(
            RESOURCES.MSGBOX_CONFIRM_DELETE_ALL_ASSOCIATIONS)
        ret = confirmbox.run()
        confirmbox.hide()
        confirmbox.destroy()
        if ret == Gtk.ResponseType.YES:
            association_ids = retrieve_association_ids()
            for x in association_ids:
                li = retrieve_association(x)
                plugin_cond = retrieve_plugin(li[0])
                plugin_task = retrieve_plugin(li[1])
                unregister_plugin_data(plugin_cond)
                unregister_plugin_data(plugin_task)
                unstore_association(x)
            self.selected_association = None
            self.fill_listAssociations(None)
            self.fill_cbSelectUninstallPlugin(None)
            o('txtCondition').set_text("")
            o('txtConsequence').set_text("")

    def click_btnEnable(self, obj):
        enable_association_id(self.selected_association, True)
        self.fill_listAssociations(None)

    def click_btnDisable(self, obj):
        enable_association_id(self.selected_association, False)
        self.fill_listAssociations(None)

    def click_btnRefresh(self, obj):
        self.fill_listHistory(None)

    def click_btnChoosePackage(self, obj):
        o = self.builder.get_object
        filter_wwpz = Gtk.FileFilter()
        filter_wwpz.set_name(RESOURCES.FILTER_PLUGIN_PACKAGE_NAME)
        filter_wwpz.add_pattern(RESOURCES.FILTER_PLUGIN_PACKAGE_PATTERN)
        dlg = Gtk.FileChooserDialog(
            RESOURCES.UI_TITLE_CHOOSE_PACKAGE_FILE, None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dlg.add_filter(filter_wwpz)
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        if filename:
            o('txtChoosePackage').set_text(filename)

    def click_btnChooseIDF(self, obj):
        o = self.builder.get_object
        filter_widf = Gtk.FileFilter()
        filter_widf.set_name(RESOURCES.FILTER_IDF_NAME)
        filter_widf.add_pattern(RESOURCES.FILTER_IDF_PATTERN)
        dlg = Gtk.FileChooserDialog(
            RESOURCES.UI_TITLE_CHOOSE_IDF_FILE, None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dlg.add_filter(filter_widf)
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        if filename:
            o('txtChooseIDF').set_text(filename)

    def click_btnInstall(self, obj):
        o = self.builder.get_object
        if self.install_package:
            if not install_plugin(self.install_package):
                box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                        buttons=Gtk.ButtonsType.OK)
                box.set_markup(RESOURCES.MSGBOX_ERR_INSTALL_PLUGIN)
            else:
                box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                        buttons=Gtk.ButtonsType.OK)
                box.set_markup(RESOURCES.MSGBOX_OK_INSTALL_PLUGIN)
                o('txtChoosePackage').set_text("")
                for name in user_plugins_names():
                    m = load_plugin_module(name)
                    if m:
                        all_plugins[name] = m.Plugin()
                self.install_package = None
                self.fill_cbSelectUninstallPlugin(None)
            box.run()
            box.hide()
            box.destroy()

    def click_btnUninstall(self, obj):
        o = self.builder.get_object
        if self.selected_uninstallplugin:
            confirmbox = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                           buttons=Gtk.ButtonsType.YES_NO)
            confirmbox.set_markup(
                RESOURCES.MSGBOX_CONFIRM_UNINSTALL_PLUGIN %
                self.selected_uninstallplugin)
            ret = confirmbox.run()
            confirmbox.hide()
            confirmbox.destroy()
            if ret == Gtk.ResponseType.YES:
                if not uninstall_plugin(self.selected_uninstallplugin):
                    box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.MSGBOX_ERR_UNINSTALL_PLUGIN)
                else:
                    box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.MSGBOX_OK_UNINSTALL_PLUGIN)
                    del all_plugins[self.selected_uninstallplugin]
                    self.selected_uninstallplugin = None
                    o('txtUninstallPluginName').set_text("")
                    o('txtUninstallPluginDescription').set_text("")
                    o('btnUninstall').set_sensitive(False)
                    self.fill_cbSelectUninstallPlugin(None)
                box.run()
                box.hide()
                box.destroy()

    def click_btnImport(self, obj):
        o = self.builder.get_object
        error = None
        if self.import_idf:
            name = os.path.basename(self.import_idf)
            if not os.path.exists(self.import_idf):
                error = RESOURCES.MSGBOX_ERR_IMPORT_IDF_READ
            elif idf_exists(name):
                error = RESOURCES.MSGBOX_ERR_IMPORT_IDF_EXISTS
            else:
                try:
                    with open(self.import_idf) as f:
                        full_contents = f.read()
                    text, params = param_file(full_contents)
                    if params:
                        box = ConfigIDFWindow(params)
                        try:
                            box.run()
                            param_dict = box.values
                            if param_dict is not None:
                                contents = replace_params(text, param_dict)
                            else:
                                error = RESOURCES.MSGBOX_ERR_IMPORT_IDF_CANCEL
                        except ValueError:
                            error = RESOURCES.MSGBOX_ERR_IMPORT_IDF_PARAMS
                        box.destroy()
                    else:
                        contents = full_contents
                except:
                    error = RESOURCES.MSGBOX_ERR_IMPORT_IDF_READ
            if error is None:
                if not idf_install(name, contents):
                    box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.MSGBOX_ERR_IMPORT_IDF)
                else:
                    box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.MSGBOX_OK_IMPORT_IDF)
                    o('txtChooseIDF').set_text("")
                    self.import_idf = None
                    self.fill_cbSelectUnimport(None)
            else:
                box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                        buttons=Gtk.ButtonsType.OK)
                box.set_markup(error)
            box.run()
            box.hide()
            box.destroy()

    def click_btnUnimport(self, obj):
        o = self.builder.get_object
        if self.selected_unimportidf:
            confirmbox = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                           buttons=Gtk.ButtonsType.YES_NO)
            confirmbox.set_markup(
                RESOURCES.MSGBOX_CONFIRM_UNIMPORT_ITEMS %
                self.selected_unimportidf)
            ret = confirmbox.run()
            confirmbox.hide()
            confirmbox.destroy()
            if ret == Gtk.ResponseType.YES:
                if idf_remove(self.selected_unimportidf) <= 0:
                    box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.MSGBOX_ERR_UNIMPORT_IDF)
                else:
                    box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.MSGBOX_OK_UNIMPORT_IDF)
                    self.selected_unimportidf = None
                    o('btnUnimport').set_sensitive(False)
                    self.fill_cbSelectUnimport(None)
                box.run()
                box.hide()
                box.destroy()

    def click_btnSchedulerApply(self, obj):
        o = self.builder.get_object
        all_options = []
        errors = []
        if o('chkGenericSettings').get_active():
            all_options.append(WHEN_OPTIONS_GENERIC)
        if o('rbScheduleNormal').get_active():
            all_options.append(WHEN_OPTIONS_REACTIVITY_NORMAL)
        else:
            all_options.append(WHEN_OPTIONS_REACTIVITY_LAZY)
        if o('chkDesktopIcons').get_active():
            if not write_desktop_entry(_WIZARD_WIZARD_SUBCOMMAND,
                                       RESOURCES.DESKTOP_ENTRY_WIZARD_NAME,
                                       _WIZARD_WIZARD_ICON,
                                       RESOURCES.DESKTOP_ENTRY_WIZARD_COMMENT) or \
               not write_desktop_entry(_WIZARD_MANAGER_SUBCOMMAND,
                                       RESOURCES.DESKTOP_ENTRY_MANAGER_NAME,
                                       _WIZARD_MANAGER_ICON,
                                       RESOURCES.DESKTOP_ENTRY_MANAGER_COMMENT):
                errors.append(RESOURCES.MSGBOX_ERR_DESKTOP_ICONS)
        if all_options:
            if not when_apply_options(all_options):
                errors.append(RESOURCES.MSGBOX_ERR_DBUS_APPLYCHANGES)
        if errors:
            errstr = "\n".join(errors)
            box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                    buttons=Gtk.ButtonsType.OK)
            box.set_markup(errstr)
        else:
            box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                    buttons=Gtk.ButtonsType.OK)
            box.set_markup(RESOURCES.MSGBOX_OK_APPLYCHANGES)
        box.run()
        box.hide()
        box.destroy()

    def changed_action_rbInstall(self, obj):
        o = self.builder.get_object
        if o('rbInstall').get_active():
            o('boxInstall').set_visible(True)
            o('boxUninstall').set_visible(False)
        else:
            o('boxInstall').set_visible(False)
            o('boxUninstall').set_visible(True)

    def changed_action_rbImport(self, obj):
        o = self.builder.get_object
        if o('rbImport').get_active():
            o('boxImport').set_visible(True)
            o('boxUnimport').set_visible(False)
        else:
            o('boxImport').set_visible(False)
            o('boxUnimport').set_visible(True)

    def click_btnQuit(self, obj):
        self.dialog.hide()
        Gtk.main_quit()

    # wizard window main function
    def run(self):
        self.dialog.present()
        ret = self.dialog.run()
        self.dialog.hide()
        return ret


# the item definition file configuration dialog box: first define auxiliary
# widget classes and then the main class; the auxiliary classes are used to
# create the widgets that are appended inside the parameter list
class entry_Text(object):

    def __init__(self, param_name, label, default):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.widget = o('entry_boxText')
        self.param_name = param_name
        self.value = default
        o('lbl_boxText').set_text(label)
        o('txt_boxText').set_text(self.value)
        o('txt_boxText').connect('changed', self.change_text)

    def change_text(self, obj):
        o = self.builder.get_object
        self.value = o('txt_boxText').get_text()


class entry_Integer(object):

    def __init__(self, param_name, label, default):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.widget = o('entry_boxInteger')
        self.param_name = param_name
        self.value = default
        o('lbl_boxInteger').set_text(label)
        o('txt_boxInteger').set_text(self.value)
        o('txt_boxInteger').connect('changed', self.change_text)

    def change_text(self, obj):
        o = self.builder.get_object
        self.value = o('txt_boxInteger').get_text()


class entry_Real(object):

    def __init__(self, param_name, label, default):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.widget = o('entry_boxReal')
        self.param_name = param_name
        self.value = default
        o('lbl_boxReal').set_text(label)
        o('txt_boxReal').set_text(self.value)
        o('txt_boxReal').connect('changed', self.change_text)

    def change_text(self, obj):
        o = self.builder.get_object
        self.value = o('txt_boxReal').get_text()


class entry_File(object):

    def __init__(self, param_name, label, default):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.widget = o('entry_boxFile')
        self.param_name = param_name
        self.value = default
        o('lbl_boxFile').set_text(label)
        o('txt_boxFile').set_text(self.value)
        o('txt_boxFile').connect('changed', self.change_text)
        o('btn_boxFile').connect('clicked', self.click_choose)

    def change_text(self, obj):
        o = self.builder.get_object
        self.value = o('txt_boxFile').get_text()

    def click_choose(self, obj):
        dlg = Gtk.FileChooserDialog(
            RESOURCES.UI_TITLE_CHOOSE_IDF_FILE, None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        o = self.builder.get_object
        o('txt_boxFile').set_text(filename)


class entry_Dir(object):

    def __init__(self, param_name, label, default):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.widget = o('entry_boxDir')
        self.param_name = param_name
        self.value = default
        o('lbl_boxDir').set_text(label)
        o('txt_boxDir').set_text(self.value)
        o('txt_boxDir').connect('changed', self.change_text)
        o('btn_boxDir').connect('clicked', self.click_choose)

    def change_text(self, obj):
        o = self.builder.get_object
        self.value = o('txt_boxDir').get_text()

    def click_choose(self, obj):
        dlg = Gtk.FileChooserDialog(
            RESOURCES.UI_TITLE_CHOOSE_IDF_FILE, None,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        res = dlg.run()
        filename = None
        if res == Gtk.ResponseType.OK:
            filename = dlg.get_filename()
        dlg.destroy()
        o = self.builder.get_object
        o('txt_boxDir').set_text(filename)


class entry_Choice(object):

    def __init__(self, param_name, label, default, choices):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.widget = o('entry_boxChoice')
        self.param_name = param_name
        self.value = default
        self.choices = choices
        o('lbl_boxChoice').set_text(label)
        cb = o('cb_boxChoice')
        for choice in choices:
            cb.append_text(choice)
        cb.set_active(choices.index(default))

    def change_value(self, obj):
        o = self.builder.get_object
        self.value = self.choices[o('cb_boxChoice').get_active()]


class ConfigIDFWindow(object):

    def __init__(self, params):
        self.builder = Gtk.Builder().new_from_string(
            ui_app_manager_paramidf, -1)
        self.builder.connect_signals(self)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.dialog = o('dlgConfigItems')
        icon = load_pixbuf(_WIZARD_MANAGER_DLGICON)
        self.dialog.set_icon(icon)
        self.ctl_dict = {}
        self.chk_dict = {}
        self.values = None

        scroll = o('boxEntries')
        for param in params:
            param_name = param[1:]
            param_type, desc, default, ctl, choices = params[param]
            if param_type == 'string':
                entry = entry_Text(param_name, desc, default)
            elif param_type == 'integer':
                entry = entry_Integer(param_name, desc, default)
            elif param_type == 'real':
                entry = entry_Real(param_name, desc, default)
            elif param_type == 'choice':
                entry = entry_Choice(param_name, desc, default, choices)
            elif param_type == 'file':
                entry = entry_File(param_name, desc, default)
            elif param_type == 'directory':
                entry = entry_Dir(param_name, desc, default)
            self.ctl_dict[param] = entry
            self.chk_dict[param] = ctl
            scroll.pack_start(entry.widget, False, False, 0)
        scroll.pack_start(o('fixFiller'), True, True, 0)

    def run(self):
        self.values = {}
        ret = self.dialog.run()
        self.dialog.hide()
        if ret == ACTION_OK:
            for k in self.ctl_dict:
                v = self.ctl_dict[k].value
                try:
                    correct = self.chk_dict[k](v)
                except:
                    raise ValueError
                if correct:
                    self.values[k] = v
                else:
                    raise ValueError
        else:
            self.values = None

    def destroy(self):
        self.dialog.destroy()


# The main application loader
class ManagerApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id=APP_ID,
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.register(None)
        self.connect('activate', self.app_activate)

    def app_activate(self, app_instance):
        self.main()

    def main(self):
        main_window = ManagerAppWindow()
        return main_window.run()


# end.
