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
    retrieve_association, retrieve_association_ids

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
            o('btnDelete').set_sensitive(False)

    def click_btnDelete(self, obj):
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
                o('txtCondition').set_text("")
                o('txtConsequence').set_text("")

    def click_btnDeleteAll(self, obj):
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
            o('txtCondition').set_text("")
            o('txtConsequence').set_text("")

    def click_btnRefresh(self, obj):
        self.fill_listHistory(None)

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
