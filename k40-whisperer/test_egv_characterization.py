from random import randint
from unittest import TestCase

from egv import egv
from original_egv import original_egv

RIGHT = 66  # ord("B")=66
LEFT = 84  # ord("T")=84
UP = 76  # ord("L")=76
DOWN = 82  # ord("R")=82
ANGLE = 77  # ord("M")=77
ON = 68  # ord("D")=68
OFF = 85  # ord("U")=85
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]


class TestEgv(TestCase):
    """
    This test compares the results of the refactor code with the results of the original code
    """

    def setUp(self):
        self.refactored_captured_data = []
        self.original_captured_data = []
        self.egv = egv(lambda s: self.refactored_captured_data.append(s))
        self.original = original_egv(lambda s: self.original_captured_data.append(s))

    def test_move(self):
        """
        sending any of the four directions return an array composed of
        :return:
        """
        direction_index = randint(0, len(DIRECTIONS) - 1)
        distance = randint(0, 255)
        laser_on = False
        angle_dirs = [randint(0, 255), randint(0, 255)]
        self.egv.move(DIRECTIONS[direction_index], distance, laser_on, angle_dirs)
        self.egv.flush(laser_on)
        distance_output = self.original.make_distance(distance)
        self.assertEqual(self.refactored_captured_data, [DIRECTIONS[direction_index]] + distance_output)

    def test_make_cut_line(self):
        dx = randint(-10000, 10000)
        dy = randint(-10000, 10000)
        self.egv.make_cut_line(dx, dy, True)
        self.egv.flush(True)
        # Do assertions

    def test_compute_horizontal_direction(self):
        self.assertEqual(self.egv.compute_x_axis_direction(1), self.egv.RIGHT)
        self.assertEqual(self.egv.compute_x_axis_direction(-1), self.egv.LEFT)

    def test_assert_integer_value(self):
        random = randint(-100, 100) / 1000
        self.assertRaises(Exception, self.egv.assert_integer_value, random)

    def test_make_speed_laser_m2(self):
        self.assert_all_known_boards(0.1, 0)
        self.assert_all_known_boards(0.1, 1)

        self.assert_all_known_boards(6, 0)
        self.assert_all_known_boards(6, 1)

        self.assert_all_known_boards(9, 0)
        self.assert_all_known_boards(9, 1)

        self.assert_all_known_boards(10, 0)
        self.assert_all_known_boards(10, 1)

        self.assert_all_known_boards(255, 0)
        self.assert_all_known_boards(255, 1)

        self.assertRaises(Exception, self.egv.make_speed, (0.1, 0, 'SOME UNKNOWN_LASER'))

    def assert_all_known_boards(self, feed, raster_step):
        self.assert_make_speed_parameters(feed, raster_step, "LASER-M2")
        self.assert_make_speed_parameters(feed, raster_step, "LASER-M1")
        self.assert_make_speed_parameters(feed, raster_step, "LASER-M")
        self.assert_make_speed_parameters(feed, raster_step, "LASER-B2")
        self.assert_make_speed_parameters(feed, raster_step, "LASER-B1")
        self.assert_make_speed_parameters(feed, raster_step, "LASER-B")

    def assert_make_speed_parameters(self, feed, raster_step, board_name):
        result = self.egv.make_speed(feed, board_name=board_name, Raster_step=raster_step)
        self.assertEqual(result, self.original.make_speed(feed, board_name=board_name, Raster_step=raster_step))
