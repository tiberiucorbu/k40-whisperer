from math import floor
from random import randint
from unittest import TestCase

from egv import egv

RIGHT = 66  # ord("B")=66
LEFT = 84  # ord("T")=84
UP = 76  # ord("L")=76
DOWN = 82  # ord("R")=82
ANGLE = 77  # ord("M")=77
ON = 68  # ord("D")=68
OFF = 85  # ord("U")=85
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]


class TestEgv(TestCase):

    def setUp(self):
        self.captured_data = []
        self.egv = egv(lambda s: self.captured_data.append(s))

    def make_distance(self, dist_mils):
        dist_mils = float(dist_mils)
        if abs(dist_mils - round(dist_mils, 0)) > 0.000001:
            raise RuntimeError('Distance values should be integer value (inches*1000)')
        DIST = 0.0
        code = []
        v122 = 255
        dist_milsA = int(dist_mils)

        for i in range(0, int(floor(dist_mils / v122))):
            code.append(122)
            dist_milsA = dist_milsA - v122
            DIST = DIST + v122
        if dist_milsA == 0:
            pass
        elif dist_milsA < 26:  # codes  "a" through  "y"
            code.append(96 + dist_milsA)
        elif dist_milsA < 52:  # codes "|a" through "|z"
            code.append(124)
            code.append(96 + dist_milsA - 25)
        elif dist_milsA < 255:
            num_str = "%03d" % (int(round(dist_milsA)))
            code.append(ord(num_str[0]))
            code.append(ord(num_str[1]))
            code.append(ord(num_str[2]))
        else:
            raise RuntimeError("Error in EGV make_distance_in(): dist_milsA=", dist_milsA)
        return code

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
        distance_output = self.make_distance(distance)
        self.assertEqual(self.captured_data, [DIRECTIONS[direction_index]] + distance_output)
