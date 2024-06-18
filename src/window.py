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
import sys
import asyncio
import logging
from playsound import playsound
from random import choice
from xml.sax.saxutils import escape
from gi.repository import Adw
from gi.repository import Gtk, GObject, Gio, GLib
from stmp import STMPServer
from stmp.interfaces import Packet, Peer

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

STMP_ROUTE="/sitty-talky-gtk"

WELCOME_MSGS = [
    "Pollute your local traffic by sending a message!",
    "Spread your sweet message over the LAN",
    "Spread a revolutionary message over the LAN",
    "Let the office know your voice!",
    "Hurry-up your peers are waiting for you!",
]

PEER_PROMPT_COLORS = [
    "#7db340", "#ff3e3e", "#0cba11", "#a5ba0c", "#ba360c", "#0cba5b", "#0c5cba",
    "#b10cba", "#ba0c19", "#ba700c", "#0ca1ba", "#ba0c42", "#ba750c", "#0ca8ba"
]
USER_COLORS = dict()


class STMPServerWorker(GObject.Object):
    def __init__(self, server:STMPServer, callback:callable=None):
        super().__init__()
        self.server = server
        self.callback = callback

    def start(self):
        task = Gio.Task.new(self, None, self.callback, None)
        task.set_return_on_cancel(False)
        task.run_in_thread(self._thread_callback)

    def _thread_callback(self, task, worker, task_data, cancellable):
        """Run the blocking operation in a worker thread."""
        print(f"Starting STMP Server")
        try:
            asyncio.run(self.server.listen_udp_async())
        except  Exception as exp:
            print(f"Error booting up server : ", exp)
        task.return_error(GLib.Error())

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

        # notification
        self.notification_sound = os.getenv("ASSETS_PATH",) + "/sounds/chat-noti.wav"
        self.notification_img = os.getenv("ASSETS_PATH",) + "/images/chat-noti.png"
        Notify.init("Sitty Talky")

        # stmp server
        self.st_server = STMPServer()
        self.st_server.route(STMP_ROUTE)(self.get_message)
        self.bind_send_btn_event(self.send_message)
        stp_logger = logging.getLogger("stmp")
        handler = logging.StreamHandler(sys.stdout)
        stp_logger.addHandler(handler)
        stp_logger.setLevel(logging.INFO)

        worker = STMPServerWorker(self.st_server, self._handle_startup_callback)
        worker.start()

    def _handle_startup_callback(self, worker, result, handler_data):
        """Handle startup errors"""
        self.create_notification("Sitty Talky", "Error initializing service!")
        def crash_stop(*args):
            return os.sys.exit(2)

        err_modal = Gtk.Dialog()
        err_modal.set_title("Initialization Error!")
        err_modal.get_content_area().append(
            Gtk.Label(label="\nSome error occurred (unlucky you 🙃) ! \n\nTwo ways ahead"+
            "\n1️⃣ Try figure out the error and report / raise a PR to @bRuttaZz" +
            "\n2️⃣ Ping @bRuttaZz with a github issue :)"))
        err_modal.add_button("_OK", Gtk.ResponseType.OK)
        err_modal.set_default_size(550, 100)
        err_modal.connect("response", crash_stop)
        err_modal.show()

    def get_message(self, packet:Packet):
        """handle incoming messages"""
        if packet.sender not in USER_COLORS:
            USER_COLORS[packet.sender] = choice(PEER_PROMPT_COLORS)
        self.append_incoming_msg(packet.data, f'{packet.headers.user}@{packet.sender.split(".")[-1]}',
                USER_COLORS[packet.sender])

    def send_message(self, msg:str):
        """handle out going messages"""
        self.st_server.send_udp(msg, STMP_ROUTE, pass_pub_key=False)

    def append_incoming_msg(self, msg:str, sender:str, color:str):
        if self.primary_msg_bx:
            self.msg_container.remove(self.primary_msg_bx)
            self.primary_msg_bx = None
        label = Gtk.Label(margin_top=4, margin_start=10, margin_end=10)
        label.set_markup(f'<span color="{color}"><b>{escape(sender)} ></b></span> {escape(msg)}')
        label.set_wrap(True)
        label.set_xalign(0)
        self.msg_container.append(label)
        playsound(self.notification_sound)


    def append_outgoing_msg(self, msg:str):
        if self.primary_msg_bx:
            self.msg_container.remove(self.primary_msg_bx)
            self.primary_msg_bx = None
        label = Gtk.Label(margin_top=4, margin_start=10, margin_end=10)
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

    def create_notification(self, title_:str, msg:str):
        notification = Notify.Notification.new(
            title_, msg, self.notification_img
        )
        notification.set_urgency(Notify.Urgency.NORMAL)
        return notification




