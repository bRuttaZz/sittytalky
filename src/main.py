# main.py
#
# Copyright 2024 Agraj P Das
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
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import SittytalkyWindow
from lib.server import SittyTalkyServer
from lib.sender import send_message


class SittytalkyApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, asset_path:str|None):
        super().__init__(application_id='site.brutt.sittytalky',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)

        # server
        self.st_server = SittyTalkyServer()

        self.asset_path = asset_path

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = SittytalkyWindow(self.asset_path, application=self)
            self.win.bind_send_btn_event(send_message)
        self.win.present()

        # starting the server
        self.st_server.start_server()
        self.st_server.on_message(self.win.append_incoming_msg)
        # self.st_server.test_triger() # for testing

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Sitty Talky',
                                application_icon='site.brutt.sittytalky',
                                developer_name='@bRuttaZz',

                                version='0.1.0',
                                developers=['bRuttaZz https://brutt.site'],
                                copyright='🄯 2024 bRuttaZz',
                                license_type=Gtk.License.GPL_3_0)
        about.present()


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = SittytalkyApplication(os.getenv('ASSETS_PATH'))
    return app.run(sys.argv)
