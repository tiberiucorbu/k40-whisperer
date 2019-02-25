from math import sqrt
from unittest import TestCase

from k40_whisperer import ECoord

EXAMPLE_ECOORDS = [[1, 2, 1], [3, 4, 1], [7, 8, 2], [9, 10, 2], [11, 12, 3], [13, 14, 3]]

class TestECoord(TestCase):

    def setUp(self):
        self.ecoord = ECoord()

    def test_make_ecoords_empty_lines(self):
        self.ecoord.make_ecoords([])
        self.assertEqual(self.ecoord.ecoords, [])
        self.assertEqual(self.ecoord.bounds, (1e10, -1e10, 1e10, -1e10))

    def test_make_ecoords_one_line_simple(self):
        self.ecoord.make_ecoords([[0, 0, 1, 1]])
        self.assertEqual(self.ecoord.ecoords, [[0, 0, 1], [1, 1, 1]])
        self.assertEqual(self.ecoord.bounds, (0, 1, 0, 1))
        self.assertEqual(self.ecoord.len, sqrt(1 + 1))

    def test_make_ecoords_one_line(self):
        self.ecoord.make_ecoords([[1, 2, 3, 4]])
        self.assertEqual(self.ecoord.ecoords, [[1, 2, 1], [3, 4, 1]])
        self.assertEqual(self.ecoord.bounds, (1, 3, 2, 4))
        self.assertEqual(self.ecoord.len, 2.8284271247461903)

    def test_make_ecoords_one_line_floats(self):
        self.ecoord.make_ecoords([[1.01, 2.02, 3.04, 4.05]])
        self.assertEqual(self.ecoord.ecoords, [[1.01, 2.02, 1], [3.04, 4.05, 1]])
        self.assertEqual(self.ecoord.bounds, (1.01, 3.04, 2.02, 4.05))
        self.assertEqual(self.ecoord.len, 2.870853531617383)

    def test_make_ecoords_line_defined_by_more_than_4_coords(self):
        self.ecoord.make_ecoords([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]])
        self.assertEqual(self.ecoord.ecoords, [[1, 2, 1], [3, 4, 1], [7, 8, 2], [9, 10, 2]])
        self.assertEqual(self.ecoord.bounds, (1, 9, 2, 10))
        self.assertEqual(self.ecoord.len, 5.656854249492381)

    def test_make_ecoords(self):
        self.ecoord.make_ecoords([[1, 2, 3, 4], [7, 8, 9, 10], [11, 12, 13, 14]])
        self.assertEqual(self.ecoord.ecoords, EXAMPLE_ECOORDS)
        self.assertEqual(self.ecoord.bounds, (1, 13, 2, 14))
        self.assertEqual(self.ecoord.len, 8.485281374238571)

    def test_set_ecoords_simple(self):
        self.ecoord.reset()
        self.ecoord.set_ecoords([[0, 0, 1], [1, 1, 1]])
        self.assertEqual(self.ecoord.ecoords, [[0, 0, 1], [1, 1, 1]])
        self.assertEqual(self.ecoord.bounds, (10000000000.0, -10000000000.0, 10000000000.0, -10000000000.0))
        self.assertEqual(self.ecoord.len, 0)

    def test_set_ecoords(self):
        self.ecoord.reset()
        self.ecoord.set_ecoords(EXAMPLE_ECOORDS)
        self.assertEqual(self.ecoord.ecoords, EXAMPLE_ECOORDS)
        self.assertEqual(self.ecoord.bounds, (3, 13, 4, 14))
        self.assertEqual(self.ecoord.len, 5.656854249492381)
