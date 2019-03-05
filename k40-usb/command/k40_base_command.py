#!/usr/bin/python
"""
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
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from typing import TypeVar, List

from connection.k40_usb_connection import K40UsbConnectionManager

RESPONSE = TypeVar('T')


class K40BaseCommand(object):

    def __init__(self, connection_manager: K40UsbConnectionManager):
        self.connection_manager = connection_manager

    def command_read(self, command_id: int, parameters: List[int]) -> any:
        self.connection_manager.write(command_id, parameters)
        return self.connection_manager.read()
