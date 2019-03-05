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
from collections import namedtuple
from unittest import TestCase
from unittest.mock import patch, Mock

from usb.util import ENDPOINT_OUT

from connection.k40_usb_connection import K40UsbConnectionManager, USB_ID_VENDOR, USB_ID_PRODUCT

descriptor = namedtuple('USBDescriptor', ['bEndpointAddress'])
logging.basicConfig(level=logging.DEBUG)


class TestK40UsbConnectionManager(TestCase):
    descriptor_endpoint_out_ = [descriptor(ENDPOINT_OUT)]
    mock_device = Mock(**{'get_active_configuration.return_value': {(0, 0): descriptor_endpoint_out_}})
    device_descriptor_mock = Mock()

    def setUp(self, ):
        TestK40UsbConnectionManager.mock_device.reset_mock()
        TestK40UsbConnectionManager.device_descriptor_mock.reset_mock()
        self.k40_usb_connection_manager = K40UsbConnectionManager()

    @patch('usb.core.find', return_value=mock_device)
    @patch('usb.util.find_descriptor', return_value=device_descriptor_mock)
    def test_connect(self, usb_util_find_descriptor_mock, usb_core_find_mock):
        self.k40_usb_connection_manager.device_filter = {}
        self.k40_usb_connection_manager.connect()
        usb_core_find_mock.assert_called_once_with(idVendor=USB_ID_VENDOR, idProduct=USB_ID_PRODUCT)
        usb_util_find_descriptor_mock.assert_called_once_with(self.descriptor_endpoint_out_,
                                                              custom_match=K40UsbConnectionManager.match_out_endpoint)
