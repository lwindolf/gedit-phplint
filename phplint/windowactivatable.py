# -*- coding: utf-8 -*-
# PHPLint plugin for Gedit
# Copyright (C) 2017 Lars Windolf <lars.windolf@gmx.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject, Gedit, Gio, PeasGtk

from .phplint import PHPLint
from .outputpanel import OutputPanel

class WindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "PHPLintWindowActivatable"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

        self._action = None
        self._config_panel = None
        self._phplint = None
        self._output_panel = None

    def do_activate(self):
        self._action = Gio.SimpleAction(name="check-with-phplint")
        self._action.connect("activate", self._run_phplint)
        self.window.add_action(self._action)

        self._output_panel = OutputPanel(self.window)
        bottom_panel = self.window.get_bottom_panel()
        bottom_panel.add_titled(self._output_panel,
                "PHPLintOutputPanel", "PHPLint")

        self._phplint = PHPLint()

    def do_deactivate(self):
        self._phplint = None
        self._output_panel = None

        self.window.remove_action("check-with-phplint")
        self._action = None

    def do_update_state(self):
        doc = self.window.get_active_document()
        state = False

        if doc:
            lang = doc.get_language()
            if lang and lang.get_id() == "php":
                state = True

        self._action.set_enabled(state)
        if state:
            self._output_panel.show()
        else:
            self._output_panel.hide()

    def _run_phplint(self, action, data=None):
        doc = self.window.get_active_document()
        if doc:
            # Show PHPLint panel if not visible
            bottom_panel = self.window.get_bottom_panel()
            if not bottom_panel.is_visible():
                bottom_panel.set_visible(True)
            if bottom_panel.get_visible_child() != self._output_panel:
                bottom_panel.set_visible_child(self._output_panel)

            # Update the panel
            report = self._phplint.run(self.window.get_active_document())
            self._output_panel.update(report)
