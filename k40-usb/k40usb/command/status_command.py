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

import logging
from typing import List

from k40usb.command.k40_base_command import K40BaseCommand
from k40usb.connection import K40UsbConnectionManager

STATUS_COMMAND_ID = 0xA0


class StatusResponse(object):
    def __init__(self, response: List[int]):
        self.raw_data = response


class StatusCommand(K40BaseCommand):

    def request_status(self) -> StatusResponse:
        raw_data = self.command_read(STATUS_COMMAND_ID, [])
        logging.debug('got raw data %s', raw_data)
        return StatusResponse(raw_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    command = StatusCommand(K40UsbConnectionManager())
    command.request_status();
