# file: share/when-wizard/lib/manager.py
# -*- coding: utf-8 -*-
#
# Implement the Wizard Manager application
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
    load_plugin_module, unstore_association, unregister_plugin_data, \
    retrieve_action_history, retrieve_plugin_data, retrieve_plugin, \
    active_plugins_names, retrieve_association, retrieve_association_ids, \
    install_plugin, uninstall_plugin

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


# the main wizard manager window
class ManagerAppWindow(object):

    def __init__(self):
        self.builder = Gtk.Builder().new_from_string(ui_app_manager, -1)
        self.builder.connect_signals(self)
        self.builder.set_translation_domain(APP_NAME)
        o = self.builder.get_object
        self.dialog = o('dlgManager')
        icon = load_pixbuf('alarmclock_wand')
        self.glyph_success = load_pixbuf('success')
        self.glyph_failure = load_pixbuf('failure')
        self.dialog.set_icon(icon)

        self.dialog_about = o('dlgAbout')
        self.dialog_about.set_icon(icon)
        self.dialog_about.set_logo(load_pixbuf('alarmclock_wand-128'))
        self.dialog_about.set_program_name(APP_SHORTNAME)
        self.dialog_about.set_website(APP_URL)
        self.dialog_about.set_copyright(APP_COPYRIGHT)
        self.dialog_about.set_comments(APP_LONGDESC)
        self.dialog_about.set_version(APP_VERSION)

        # dialog data
        self.selected_association = None
        self.selected_uninstallplugin = None
        self.install_package = None

        # prepare controls
        r_text = Gtk.CellRendererText()
        r_text_e = Gtk.CellRendererText()
        r_text_e.set_property('ellipsize', Pango.EllipsizeMode.MIDDLE)
        r_pixbuf = Gtk.CellRendererPixbuf()
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

        # default sensitivity states
        o('btnDelete').set_sensitive(False)
        o('btnInstall').set_sensitive(False)
        o('btnUninstall').set_sensitive(False)
        self.change_action(None)

    def show_about(self, *data):
        self.dialog_about.present()
        self.dialog_about.run()
        self.dialog_about.hide()

    def fill_listAssociations(self, obj):
        o = self.builder.get_object
        store = Gtk.ListStore(str,
                              GdkPixbuf.Pixbuf, str,
                              GdkPixbuf.Pixbuf,
                              GdkPixbuf.Pixbuf, str)
        association_ids = retrieve_association_ids()
        arrow = load_pixbuf('right')
        l = o('listAssociation')
        delall_sensitive = False
        for x in association_ids:
            li = retrieve_association(x)
            cond_name = li[0]
            cond_data = retrieve_plugin_data(cond_name)
            cond_pixbuf = load_pixbuf(cond_data['icon'])
            task_name = li[1]
            task_data = retrieve_plugin_data(task_name)
            task_pixbuf = load_pixbuf(task_data['icon'])
            store.append([x, cond_pixbuf, cond_data['name'], arrow,
                          task_pixbuf, task_data['name']])
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

    def changed_listAssociation(self, sel):
        o = self.builder.get_object
        m, i = sel.get_selected()
        if i is not None:
            self.selected_association = m[i][0]
            li = retrieve_association(self.selected_association)
            data_cond = retrieve_plugin_data(li[0])
            data_task = retrieve_plugin_data(li[1])
            o('txtCondition').set_text(data_cond['summary_description'])
            o('txtConsequence').set_text(data_task['summary_description'])
            o('btnDelete').set_sensitive(True)
        else:
            o('txtCondition').set_text("")
            o('txtConsequence').set_text("")
            o('btnDelete').set_sensitive(False)

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
            o('txtUninstallPluginName').set_text("")
            o('txtUninstallPluginDescription').set_text("")
            o('btnUninstall').set_sensitive(False)

    def change_txtChoosePackage(self, obj):
        o = self.builder.get_object
        path = o('txtChoosePackage').get_text()
        if os.path.exists(path) and os.path.isfile(os.path.realpath(path)):
            self.install_package = path
            o('btnInstall').set_sensitive(True)
        else:
            self.install_package = None
            o('btnInstall').set_sensitive(False)

    def click_btnDelete(self, obj):
        o = self.builder.get_object
        if self.selected_association:
            confirmbox = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION,
                                           buttons=Gtk.ButtonsType.YES_NO)
            confirmbox.set_markup(
                RESOURCES.UI_MSGBOX_CONFIRM_DELETE_ASSOCIATION)
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
            RESOURCES.UI_MSGBOX_CONFIRM_DELETE_ALL_ASSOCIATIONS)
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

    def click_btnRefresh(self, obj):
        self.fill_listHistory(None)

    def click_btnChoosePackage(self, obj):
        o = self.builder.get_object
        filter_wwpz = Gtk.FileFilter()
        filter_wwpz.set_name("Plugin Packages")
        filter_wwpz.add_pattern("*.wwpz")
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

    def click_btnInstall(self, obj):
        o = self.builder.get_object
        if self.install_package:
            if not install_plugin(self.install_package):
                box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                        buttons=Gtk.ButtonsType.OK)
                box.set_markup(RESOURCES.UI_MSGBOX_ERR_INSTALL_PLUGIN)
            else:
                box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                        buttons=Gtk.ButtonsType.OK)
                box.set_markup(RESOURCES.UI_MSGBOX_OK_INSTALL_PLUGIN)
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
                RESOURCES.UI_MSGBOX_CONFIRM_UNINSTALL_PLUGIN %
                self.selected_uninstallplugin)
            ret = confirmbox.run()
            confirmbox.hide()
            confirmbox.destroy()
            if ret == Gtk.ResponseType.YES:
                if not uninstall_plugin(self.selected_uninstallplugin):
                    box = Gtk.MessageDialog(type=Gtk.MessageType.ERROR,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.UI_MSGBOX_ERR_UNINSTALL_PLUGIN)
                else:
                    box = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                            buttons=Gtk.ButtonsType.OK)
                    box.set_markup(RESOURCES.UI_MSGBOX_OK_UNINSTALL_PLUGIN)
                    del all_plugins[self.selected_uninstallplugin]
                    self.selected_uninstallplugin = None
                    o('txtUninstallPluginName').set_text("")
                    o('txtUninstallPluginDescription').set_text("")
                    o('btnUninstall').set_sensitive(False)
                    self.fill_cbSelectUninstallPlugin(None)
                box.run()
                box.hide()
                box.destroy()

    def change_action(self, obj):
        o = self.builder.get_object
        if o('rbInstall').get_active():
            o('boxInstall').set_visible(True)
            o('boxUninstall').set_visible(False)
        else:
            o('boxInstall').set_visible(False)
            o('boxUninstall').set_visible(True)

    def click_btnQuit(self, obj):
        self.dialog.hide()
        Gtk.main_quit()

    # wizard window main function
    def run(self):
        self.dialog.present()
        ret = self.dialog.run()
        self.dialog.hide()
        return ret


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
