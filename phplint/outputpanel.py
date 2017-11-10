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

import json
import sys, re
import urllib.request

from gi.repository import Gtk

__all__ = ("OutputPanel", )

class OutputPanel(Gtk.ScrolledWindow):
    """Panel to display the results of a PHPLint run."""

    def __init__(self, window):
        Gtk.ScrolledWindow.__init__(self)

        # Parent window
        self._window = window

        # Tree view
        self._tree_view = Gtk.TreeView(Gtk.ListStore(int, int, str, str))
        self._tree_view.set_headers_visible(False)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Message", renderer, text=2, background=3)
        self._tree_view.append_column(column)
        self._tree_view.connect("row-activated", self.on_row_activated)
        self.add(self._tree_view)

        self.show_all()

    def clear(self):
        """Remove all rows."""

        self._tree_view.get_model().clear()

    def on_row_activated(self, treeview, path, view_column):
        """Move cursor to the position given by the current row."""

        line, column = treeview.get_model()[path][:2]

        if line > 0 and column > 0:
            view = self._window.get_active_view()
            if view:
                buf = view.get_buffer()
                buf.place_cursor(buf.get_iter_at_line_offset(line-1, column-1))
                view.grab_focus()

    def update(self, output):
        """Update the panel with informations from the PHPLint report
        given as a JSON string.
        """
        self.clear()
        report = output.splitlines()
        if len(report) == 0:
            # No error, perfect code!
            self._tree_view.get_model().append([-1, -1,
                "No error, congrats!", "green"])
        else:
            for item in report:
                # Parse stuff like:
                #
                # PHP Parse error:  syntax error, unexpected ')', expecting end of file in a.php on line 3
                severity = "white"
                if re.search("warning:", item):
                    severity = "yellow"
                if re.search("error:", item):
                    severity = "red"

                m = re.search("on line (\d+)", item)
                if m != None:
                    line = int(m.group(1))
                else:
                    line = 0

                self._tree_view.get_model().append([ line, 0, item, severity])
