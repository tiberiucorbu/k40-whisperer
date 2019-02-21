import math
from random import randint
from unittest import TestCase
from unittest.mock import patch, Mock

from nano_library import K40_CLASS


class TestK40_CLASS(TestCase):
    mock_device = Mock(**{'get_active_configuration.return_value': {(0, 0): 'does_not_mater'}})
    device_descriptor_mock = Mock()

    @patch('usb.core.find', return_value=mock_device)
    @patch('usb.util.find_descriptor', return_value=device_descriptor_mock)
    def setUp(self, usb_core_find_mock, usb_util_find_descriptor_mock):
        self.k40Class = K40_CLASS()
        # Because any other operation depends on a valid initialization
        self.k40Class.initialize_device()
        TestK40_CLASS.mock_device.write.reset_mock()
        TestK40_CLASS.mock_device.read.reset_mock()

    def test_initialize_configuration(self):
        # just assert calls because it is called every time in setup
        TestK40_CLASS.mock_device.get_active_configuration.assert_called()

    def test_say_hello_read_device_returns_zeros(self):
        TestK40_CLASS.mock_device.configure_mock(**{'read.return_value': [0, 0, 0, 0, 0, 0, 0, 0]})
        self.assertEqual(self.k40Class.say_hello(), 9999)
        TestK40_CLASS.mock_device.write.assert_called_with(2, self.k40Class.hello, 200)

    def test_say_hello_unknown_2(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.UNKNOWN_2]})
        self.assertEqual(self.k40Class.say_hello(), self.k40Class.UNKNOWN_2)

    def test_say_hello_buffer_full(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.BUFFER_FULL]})
        self.assertEqual(self.k40Class.say_hello(), self.k40Class.BUFFER_FULL)

    def test_say_hello_CRC_ERROR(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.CRC_ERROR]})
        self.assertEqual(self.k40Class.say_hello(), self.k40Class.CRC_ERROR)

    def test_say_hello_OK(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.OK]})
        self.assertEqual(self.k40Class.say_hello(), self.k40Class.OK)

    def test_unlock_rail(self):
        self.k40Class.unlock_rail()
        TestK40_CLASS.mock_device.write.assert_called_with(2, self.k40Class.unlock, 200)

    def test_e_stop(self):
        self.k40Class.e_stop()
        TestK40_CLASS.mock_device.write.assert_called_with(2, self.k40Class.estop, 200)

    def test_home_position(self):
        self.k40Class.home_position()
        TestK40_CLASS.mock_device.write.assert_called_with(2, self.k40Class.home, 200)

    def test_reset_usb(self):
        self.k40Class.reset_usb()
        TestK40_CLASS.mock_device.reset.assert_called_once()

    @patch('usb.util.dispose_resources')
    def test_release_usb(self, usb_util__dispose_resources_mock):
        self.k40Class.release_usb()
        usb_util__dispose_resources_mock.assert_called_with(TestK40_CLASS.mock_device)

    def crcProcess(self, line):
        crc = 0
        for i in range(len(line)):
            inbyte = line[i]
            for j in range(8):
                mix = (crc ^ inbyte) & 0x01
                crc >>= 1
                if (mix):
                    crc ^= 0x8C
                inbyte >>= 1
        return crc

    def test_OneWireCRC(self):  ## Checksum
        line = [randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)]
        self.assertEqual(self.k40Class.OneWireCRC(line), self.crcProcess(line))

    def test_none_function(self):
        pass

    def test_send_data_simple_data(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.OK]})
        data = [1, 2, 3, 4, 5, 6, 7]
        self.k40Class.send_data(data)
        self.assertEqual(self.mock_device.write.mock_calls[0][1], (2,
                                                                   [166, 0, 1, 2, 3, 4, 5, 6, 7, 70, 70, 70, 70, 70, 70,
                                                                    70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                                                                    70, 70, 70, 70, 166,
                                                                    155], 200))
        self.assertEqual(self.mock_device.write.mock_calls[1][1], (2, [160], 200))

    def test_send_data_randoms_packet_count(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.OK]})
        data = []
        length = randint(5, 10) * randint(7, 32)
        for i in range(0, length):
            data.append(randint(0, 255))

        self.k40Class.send_data(data)

        packageSize = 30
        count = math.ceil(length / packageSize)

        self.assertEqual(len(self.mock_device.write.mock_calls) / 2, count)  # 2 because is one package and one check

    def test_send_data_randoms_packet_content(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.OK]})
        data = []
        length = randint(5, 10) * randint(7, 32)
        for i in range(0, length):
            data.append(randint(0, 255))

        self.k40Class.send_data(data)
        package_size = 30
        count = math.ceil(length / package_size)
        expected_data_package_prefix = [166, 0]
        for x in range(count):
            package = self.mock_device.write.mock_calls[x * 2]
            check = self.mock_device.write.mock_calls[x * 2 + 1]
            offset = x * package_size
            package_chunk = data[offset:offset + package_size]
            package_chunk = package_chunk + [70] * (package_size - len(package_chunk))
            expected_package_suffix = [166, 0]
            expected_package = expected_data_package_prefix + package_chunk + expected_package_suffix
            expected_package[-1] = self.crcProcess(expected_package[1:len(expected_package) - 2])
            sent_package = package[1][1]

            self.assertEqual(len(sent_package), len(expected_package),
                             'sent package should have the same length as the package size + 3')
            self.assertEqual(sent_package, expected_package)  # Firs argument is 166
            self.assertEqual(check[1][1][0], 160)  # first argument is 160

    def test_send_data_randoms_packet_content_preprocess_crc(self):
        TestK40_CLASS.mock_device.configure_mock(
            **{'read.return_value': [0, self.k40Class.OK]})
        data = []
        length = randint(5, 10) * randint(7, 32)
        for i in range(0, length):
            data.append(randint(0, 255))

        self.k40Class.send_data(data, None, None, 1, True, False)
        package_size = 30
        count = math.ceil(length / package_size)
        expected_data_package_prefix = [166, 0]
        for x in range(count):
            package = self.mock_device.write.mock_calls[x * 2]
            check = self.mock_device.write.mock_calls[x * 2 + 1]
            offset = x * package_size
            package_chunk = data[offset:offset + package_size]
            package_chunk = package_chunk + [70] * (package_size - len(package_chunk))
            expected_package_suffix = [166, 0]
            expected_package = expected_data_package_prefix + package_chunk + expected_package_suffix
            expected_package[-1] = self.crcProcess(expected_package[1:len(expected_package) - 2])
            sent_package = package[1][1]

            self.assertEqual(len(sent_package), len(expected_package),
                             'sent package should have the same length as the package size + 3')
            self.assertEqual(sent_package, expected_package)  # Firs argument is 166
            self.assertEqual(check[1][1][0], 160)  # first argument is 160

    #
    # def test_send_packet_w_error_checking(self):
    #     self.fail()
    #
    # def test_wait_for_laser_to_finish(self):
    #     self.fail()
    #
    # def test_send_packet(self):
    #     self.fail()
    #
    # def test_rapid_move(self):
    #     self.fail()
    #
    # def test_hex2dec(self):
    #     self.fail()
