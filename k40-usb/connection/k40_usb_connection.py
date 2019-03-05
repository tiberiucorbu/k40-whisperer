#!/usr/bin/python
"""
    Handles usb device IO to the CH341A Chip

    Copyright (C) <2019>  <@tiberiucorbu>
    Copyright (C) <2018>  <Scorch>

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

import usb
from usb.core import NoBackendError
from usb.util import endpoint_direction, ENDPOINT_OUT

WRITE_ADDRESS = 0x02
READ_ADDRESS = 0x82

CTRL_TIMEOUT = 2000
CTRL_REQUEST_VALUE = 0x0102

DEVICE_HANDLE = 0x40

CTRL_LOOPBACK_WRITE = 0xB1
# K40 boards use a CH341A see http://www.anok.ceti.pl/download/ch341ds1.pdf
USB_ID_PRODUCT = 0x5512
USB_ID_VENDOR = 0x1a86


class DeviceUnreachableError(Exception):
    pass


class USBDeviceDescriptor(object):
    pass


class K40UsbConnectionManager(object):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.dev = None

    def connect(self) -> None:
        self.maybe_release_usb()
        self.find_device()
        self.set_default_configuration()
        self.bootstrap_usb_device()
        self.check_control_transfer()

    def check_control_transfer(self) -> None:
        control_transfer_response = self.dev.ctrl_transfer(DEVICE_HANDLE, CTRL_LOOPBACK_WRITE, CTRL_REQUEST_VALUE, 0, 0,
                                                           CTRL_TIMEOUT)
        self.logger.info('received ctrl transfer : %s', control_transfer_response)

    def bootstrap_usb_device(self) -> None:
        """
        part of the usb bootstrap process, where a configuration  must be set and asserted that a write descriptor is
        present for clarifications check pyusb's tutorial : https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst


        :return: None
        """

        configuration = self.dev.get_active_configuration()
        self.logger.debug('active configuration %s', configuration)
        intf = configuration[(0, 0)]
        self.logger.debug('initial f %s', intf)
        descriptor = usb.util.find_descriptor(intf, custom_match=self.match_out_endpoint)
        if descriptor is None:
            raise Exception("Unable to match the USB 'OUT' endpoint.")
        self.logger.info('got descriptor %s', descriptor)
        assert descriptor is not None
        # self.dev.clear_halt(descriptor)

    def maybe_release_usb(self):
        if self.dev is not None:
            try:
                self.release_usb()
            except usb.USBError:
                self.logger.warning(
                    'usb device [vendor : %s, product:  %s] could\'t be released, maybe it was not locked before',
                    USB_ID_PRODUCT, USB_ID_VENDOR)
                pass

    def find_device(self) -> None:
        # find the device
        try:
            self.dev = usb.core.find(idVendor=USB_ID_VENDOR, idProduct=USB_ID_PRODUCT)
        except NoBackendError:
            self.logger.error(
                'missing usb backend, maybe libusb is not installed, '
                'see pyusb\'s readme : https://github.com/pyusb/pyusb#installing')
            raise DeviceUnreachableError()
        if self.dev is None:
            raise DeviceUnreachableError("Unable find device  [vendor : %s, product:  %s] ", USB_ID_PRODUCT,
                                         USB_ID_VENDOR)
        self.logger.info('retrieved device %s', self.dev)

    def set_default_configuration(self) -> None:
        """
            set the default configuration handled by pyusb

            :returns None
        """
        try:
            self.dev.set_configuration()
        except usb.USBError:
            # return "Unable to set USB Device configuration."
            raise Exception("Unable to set USB Device configuration.")

    @staticmethod
    def match_out_endpoint(item):
        return endpoint_direction(item.bEndpointAddress) is ENDPOINT_OUT

    def release_usb(self) -> None:
        usb.util.dispose_resources(self.dev)
        self.dev = None
        self.connection.next(self.dev)

    def ensure_connection(self) -> None:
        if self.dev is None:
            self.connect()

    def write(self, command_id, parameters) -> None:
        self.ensure_connection()
        self.dev.write(WRITE_ADDRESS, [command_id] + parameters, 2000)

    def read(self):
        self.ensure_connection()
        return self.dev.read(READ_ADDRESS, 168)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    connection_manger = K40UsbConnectionManager()
    connection_manger.connect()
