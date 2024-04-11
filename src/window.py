# window.py
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
from random import choice
from xml.sax.saxutils import escape
from gi.repository import Adw
from gi.repository import Gtk, Gdk


WELCOME_MSGS = [
    "Pollute your local traffic by sending a message!",
    "Spread your sweet message over the LAN",
    "Spread a revolutionary message over the LAN",
]

@Gtk.Template(resource_path='/site/brutt/sittytalky/window.ui')
class SittytalkyWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'SittytalkyWindow'

    msg_container = Gtk.Template.Child("msg-container")
    send_btn = Gtk.Template.Child("send_btn")
    message_box = Gtk.Template.Child("msg_entry")
    # primary welcoming msg
    primary_msg_bx = Gtk.Template.Child("primary_message")

    def __init__(self, asset_path:str|None, **kwargs):
        super().__init__(**kwargs)
        self.asset_path = asset_path
        self.primary_msg_bx.set_markup(f'<span alpha="50%">{choice(WELCOME_MSGS)}</span>')

    def append_incoming_msg(self, msg:str, sender:str):
        if self.primary_msg_bx:
            self.msg_container.remove(self.primary_msg_bx)
            self.primary_msg_bx = None
        label = Gtk.Label(margin_top=6, margin_start=10, margin_end=10)
        label.set_markup(f'<span color="#7db340"><b>[@{escape(sender)}] ></b></span> {escape(msg)}')
        label.set_wrap(True)
        label.set_xalign(0)
        self.msg_container.append(label)


    def append_outgoing_msg(self, msg:str):
        if self.primary_msg_bx:
            self.msg_container.remove(self.primary_msg_bx)
            self.primary_msg_bx = None
        label = Gtk.Label(margin_top=6, margin_start=10, margin_end=10)
        label.set_markup(f'{escape(msg)} 🔵')
        label.set_wrap(True)
        label.set_xalign(1)
        self.msg_container.append(label)

    def bind_send_btn_event(self, callback:callable):
        """Bind callback on clicking send button or other send message ui trigers"""
        def _on_btn_click(_):
            msg = self.message_box.get_text()
            self.message_box.set_text("")
            self.append_outgoing_msg(msg)
            callback(msg)

        self.send_btn.connect("clicked", _on_btn_click)
        self.message_box.connect("activate", _on_btn_click)





