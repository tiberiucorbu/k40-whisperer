#!/usr/bin/python
"""
    Entry point of the K40 usb facade

    Copyright (C) <2019>  <@tiberiucorbu>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from rx.subjects import Subject

from command.status_command import StatusCommand
from connection.k40_usb_connection import K40UsbConnectionManager


class Message(object):
    pass


class K40UsbManager(object):
    write_pipe = Subject()
    read_pipe = Subject()

    def __init__(self):
        self.connection_manager = K40UsbConnectionManager()
        self.write_pipe.subscribe(on_next=self.write_next)
        self.commands = {
            'status': StatusCommand(self.connection_manager)
        }

    def write_next(self, message: Message):
        self.connection_manager.ensure_connection()
        self.connection_manager.write(message, [])


if __name__ == "__main__":
    manager = K40UsbManager()
