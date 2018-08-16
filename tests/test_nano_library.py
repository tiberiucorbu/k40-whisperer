
""" Perform unit tests on the nano_library.py file
"""

import unittest

from k40 import nano_library

class Fake_dev:
    def __init__(self):
        self.expect = None
        self.write_data = ''

    def _handle(self, name):
        if self.expect != name:
            raise ValueError

    def reset(self):
        self._handle('reset')

    def write(self, addr, data, timeout):
        self._handle('write')
        self.write_addr = addr
        self.write_data += "".join(map(chr, data))
        self.write_timeout = timeout

    def read(self, addr, buflen, timeout):
        # TODO - this often comes after a write, so we cannot expect both
        #self._handle('write')
        self.read_addr = addr
        self.read_buflen = buflen
        self.read_timeout = timeout
        return [255,206,-1,-1,-1,-1] # 206 == self.OK

# Test command sequences
TEST_UNLOCK = map(ord, '\xa6\x00IS2PFFFFFFFFFFFFFFFFFFFFFFFFFF\xa6\x0f')
TEST_HOME = map(ord, '\xa6\x00IPPFFFFFFFFFFFFFFFFFFFFFFFFFFF\xa6\xe4')
TEST_ESTOP = map(ord, '\xa6\x00IFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\xa6\x82')

class TestK40Interface(unittest.TestCase):
    def setUp(self):
        self.object = nano_library.K40Interface()
        self.object.dev = Fake_dev()

    def tearDown(self):
        self.object = None

    def test_hello(self):
        self.object.dev.expect = 'write'
        self.assertEqual(self.object.hello(), nano_library._RESP_OK)
        self.assertEqual(
            self.object.dev.write_data,
            '\xa0'
        )

    # Several of these function calls have nested calls to dev functions,
    # which my dumb dev mock cannot handle:
    #   unlock_rail() calls say_hello()
    #   e_stop() calls say_hello()
    #   home_position() calls say_hello()

    def test_reset_usb(self):
        self.object.dev.expect = 'reset'
        self.object.reset()

    def test_crc(self):
        line = map(ord, 'AK0FFFFFFFFFFFFFFFFFFFFFFFFFFF')

        # Do we get the expected CRC?
        self.assertEqual( nano_library._crc(line), 0xa4 )

        # Now, are the magic arrays simply normal packets with a valid CRC?
        self.assertEqual(
            nano_library._crc(TEST_UNLOCK[1:-2]),
            TEST_UNLOCK[-1] 
        )
        self.assertEqual(
            nano_library._crc(TEST_HOME[1:-2]),
            TEST_HOME[-1] 
        )
        self.assertEqual(
            nano_library._crc(TEST_ESTOP[1:-2]),
            TEST_ESTOP[-1] 
        )

    def test_send_data(self):
        data = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        self.object.dev.expect = 'write'
        self.object.send_data(map(ord, data))

        packet_marker = '\xa6'
        packet_end = '\xa0'
        packet_data1 = data[0:30]
        packet_data2 = data[30:52]

        packet_data2 += 'FFFFFFFF'  # fill data to a full packet size

        expect = packet_marker + '\x00' + packet_data1 + packet_marker
        expect += chr(nano_library._crc(map(ord, packet_data1)))
        expect += packet_end

        expect += packet_marker + '\x00' + packet_data2 + packet_marker
        expect += chr(nano_library._crc(map(ord, packet_data2)))
        expect += packet_end

        self.assertEqual(
            expect,
            self.object.dev.write_data
        )

        # FIXME - where is the second packet?

    def test_rapid_move(self):
        self.object.dev.expect = 'write'
        self.object.rapid_move(1000, 1000)

        # Deeper probing of this data block is done in test_egv
        expect = '\xa6\x00ILzzz235Bzzz235S1PFFFFFFFFFFFF\xa6\x8a\xa0'
        self.assertEqual(self.object.dev.write_data, expect)
