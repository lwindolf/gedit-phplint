# -*- coding: utf-8 -*-
#    PHPLint plugin for Gedit
#    Copyright (C) 2017 Lars Windolf <lars.windolf@gmx.de>
#    Copyright (C) 2016 Xavier Gendre <gendre.reivax@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import shlex
import subprocess
import sys
import tempfile

__all__ = ("PHPLint", )

class PHPLint(object):

    def run(self, doc):
        """Run "php -l" on the content of the GeditDocument
        Return a JSON string containing the PHPLint
        report or an empty object if an error occurred.
        """

        text = doc.get_text(
                doc.get_start_iter(),
                doc.get_end_iter(),
                True).encode()

        with tempfile.NamedTemporaryFile() as f:
            f.write(text)
            f.flush()

            cmd = ' '.join([
                'php',
                '-l',
                f.name])
            cmd_array = shlex.split(cmd)

            try:
                p = subprocess.Popen(cmd_array, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                return err.strip()
            except OSError as e:
                print(' '.join(["PHPLint Plugin:", e.strerror]),
                        file=sys.stderr)
                return ""

