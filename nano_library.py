#!/usr/bin/env python
'''This module implements low-level communications with a K40 laser cutter.'''

# Copyright (C) 2017 Scorch www.scorchworks.com
# Copytight (C) 2017 Serge 'q3k' Bazanski <serge@bazanski.pl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import logging
import math

import usb.core
import usb.util

from egv import egv


logger = logging.getLogger('k40whisperer.interface')
logger.setLevel(logging.DEBUG)


def _crc(line):
    """
    CRC algorithm derived from OneWire.cpp.

    Latest version of library can be found at
    http://www.pjrc.com/teensy/td_libs_OneWire.html .
    """
    crc = 0
    for char in line:
        for _ in range(8):
            mix = (crc ^ char) & 0x01
            crc >>= 1
            if (mix):
                crc ^= 0x8C
            char >>= 1
    return crc


_TYPE_HELLO = 160
_TYPE_DATA = 166
_TYPE_RESP = 255


def _data_packet(data):
    if len(data) > 30:
        raise Exception("Data too long to fit in packet")

    res = []
    res.append(_TYPE_DATA)
    res.append(0)  # always zero?
    for d in data:
        res.append(ord(d))
    # packet is always 34 bytes (including CRC, header, terminator and zero)
    res += [70 for _ in range(32 - len(res))]
    res.append(_TYPE_DATA)
    res.append(_crc(res[1:-1]))
    return res


_CMD_HELLO = [_TYPE_HELLO, ]
_CMD_UNLOCK = _data_packet('IS2P')
_CMD_HOME = _data_packet('IPP')
_CMD_ESTOP = _data_packet('I')

_RESP_OK = 206
_RESP_BUFFER_FULL = 238
_RESP_CRC_ERROR = 207
_RESP_UNKNOWN_1 = 236
# After failed initialization followed by succesful initialization
_RESP_UNKNOWN_2 = 239


class K40Interface(object):

    HELLO_RESPONSE_SIZE = 168

    def __init__(self):
        self.dev = None

        self.n_timeouts = 10
        self.timeout = 200  # Time in milliseconds

        self.write_addr = 0x2
        self.read_addr = 0x82

    def _device_read(self, length):
        res = self.dev.read(self.read_addr, length, self.timeout)
        logger.debug('Response: {}'.format(res))
        return res

    def _device_write(self, data):
        logger.debug('Request: {}'.format(data))
        self.dev.write(self.write_addr, data, self.timeout)

    def reset(self):
        self.dev.reset()

    def release(self):
        usb.util.dispose_resources(self.dev)
        self.dev = None

    def hello(self):
        """
        Sends a hello message to the device and returns response code (if
        correct).
        """
        for _ in range(self.n_timeouts):
            try:
                self._device_write(_CMD_HELLO)
                break
            except Exception as e:
                logger.info("Could not send to device: {}".format(e))
                pass
        else:
            msg = ("Too Many Transmission Errors ({:d} Status Timeouts)"
                   .format(self.n_timeouts))
            raise StandardError(msg)

        response = None
        try:
            while response is None:
                response = self._device_read(self.HELLO_RESPONSE_SIZE)
        except Exception as e:
            logger.error("Failed to read from device: {}".format(e))
            return None

        if response[1] in [_RESP_OK, _RESP_BUFFER_FULL, _RESP_CRC_ERROR,
                           _RESP_UNKNOWN_1, _RESP_UNKNOWN_2]:
            return response[1]
        return None

    def unlock_rail(self):
        self._device_write(_CMD_UNLOCK)

    def e_stop(self):
        self._device_write(_CMD_ESTOP)

    def home_position(self):
        self._device_write(_CMD_HOME)

    def send_data(self, data, update_gui=lambda x: None):
        packets = []

        # Split data into blocks to fit into packets.
        block_size = 30
        block_count = int(math.ceil(float(len(data)) / block_size))
        for i in range(0, len(data), block_size):
            update_gui("Calculating CRC and generating packets: {:.1f}%"
                       .format(100 * i / block_count))

            packet = ''.join(chr(c) for c in data[i:i+block_size])
            packets.append(_data_packet(packet))

        for i, packet in enumerate(packets):
            update_gui("Sending data to Laser: {:.1f}%"
                       .format(100.0 * i / len(packets)))
            self._send_packet_retry(packet, update_gui=update_gui)

    def _send_packet_retry(self, packet, update_gui=lambda x: None):
        for retry in range(self.n_timeouts):
            try:
                self._device_write(packet)
            except Exception as e:
                logger.info("Could not write to device: {}".format(e))
                update_gui("USB Timeout #{}".format(retry))
                continue

            response = self.hello()

            while response == _RESP_BUFFER_FULL:
                response = self.hello()

            if response == _RESP_CRC_ERROR:
                update_gui("Data transmission (CRC) error #{}".format(retry))
                continue

            break
        else:
            msg = "Too many transmission errors ({})".format(retry)
            update_gui(msg)
            raise StandardError(msg)

    def rapid_move(self, dxmils, dymils):
        data = []
        egv_inst = egv(target=lambda s: data.append(s))
        egv_inst.make_move_data(dxmils, dymils)
        self.send_data(data)

    def initialize_device(self):
        try:
            self._device_release()
        except:
            pass

        self.dev = usb.core.find(idVendor=0x1a86, idProduct=0x5512)
        if self.dev is None:
            raise StandardError("Laser USB Device not found.")
        logger.debug('Device: {}'.format(self.dev))

        try:
            self.dev.set_configuration()
        except:
            raise StandardError("Unable to set USB Device configuration.")

        cfg = self.dev.get_active_configuration()
        logger.debug('Configuration: {}'.format(cfg))

        interface = cfg[(0, 0)]
        logger.debug('Interface: {}'.format(interface))

        def match(e):
            direction = usb.util.endpoint_direction(e.bEndpointAddress)
            return direction == usb.util.ENDPOINT_OUT

        endpoint = usb.util.find_descriptor(interface, custom_match=match)
        if endpoint is None:
            raise StandardError("Unable to match the USB 'OUT' endpoint.")
        logger.debug('Endpoint: {}'.format(endpoint))

        ctrlxfer = self.dev.ctrl_transfer(0x40, 177, 0x0102, 0, 0, 2000)
        logger.debug('Control transfer result: {}'.format(ctrlxfer))


if __name__ == "__main__":
    k40 = K40Interface()

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    k40.initialize_device()
    k40.hello()
    k40.home_position()
    k40.rapid_move(1000, -1000)
