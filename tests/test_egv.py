
""" Perform unit tests on the egv.py file
"""


import unittest

from k40 import egv, K40Exception

class TestegvClass(unittest.TestCase):
    def setUp(self):
        self.object = egv.egv(target=lambda s:self.data.append(s))
        self.data = bytearray()

    def tearDown(self):
        self.object = None

    def test_move(self):

        tests = [
            { 'dir':        0, 'dist':  0, 'laser': False, 'expect': b'' },
            { 'dir': ord('B'), 'dist':  1, 'laser': False, 'expect': b'Ba' },
            { 'dir': ord('T'), 'dist':  1, 'laser': False, 'expect': b'Ta' },
            { 'dir': ord('L'), 'dist':  1, 'laser': False, 'expect': b'La' },
            { 'dir': ord('R'), 'dist':  1, 'laser': False, 'expect': b'Ra' },
            { 'dir': ord('M'), 'dist':  1, 'laser': False, 'expect': b'Ma' },
            { 'dir':  0, 'dist':  0, 'laser': True,  'expect': b'D' },
            { 'dir':  0, 'dist':  0, 'laser': False, 'expect': b'U' },
        ]

        # TODO
        # - need to write code to exercise the angle_dirs, but I dont quite
        #   understand what they are trying to achieve yet

        for test in tests:
            self.data = bytearray()
            self.object.move( test['dir'], test['dist'], test['laser'] )
            self.object.flush()
            self.assertEqual( self.data, test['expect'] )

    def test_flush(self):
        tests = [
            { 'laser': False, 'expect': b'' },
            { 'laser': True,  'expect': b'D' },
            { 'laser': False, 'expect': b'U' },
        ]

        for test in tests:
            self.data = bytearray()
            self.object.flush(laser_on=test['laser'])
            self.assertEqual( self.data, test['expect'] )

#
# This file has a syntax error in OneWireCRC - the return tries to return
# an undefined variable.
#
# Thus - assume that function is unused for the moment
#
#    def test_OneWireCRC(self):
#        self.assertEqual(
#            self.object.OneWireCRC([fixme]),
#            fixme
#        )

    def test_make_distance(self):
        with self.assertRaises(K40Exception):
            self.object.make_distance(1.1)

        # What a strange number coding.  I guess they had never heard of
        # Huffman, or ASN.1 BER
        tests = [
            { 'mils':    0, 'expect': b'' },
            { 'mils':    1, 'expect': b'a' },
            { 'mils':   25, 'expect': b'y' },
            { 'mils':   26, 'expect': b'|a' },
            { 'mils':   51, 'expect': b'|z' },
            { 'mils':   52, 'expect': b'052' },
            { 'mils':  254, 'expect': b'254' },
            { 'mils':  255, 'expect': b'z' },
            { 'mils':  256, 'expect': b'za' },
            { 'mils':  511, 'expect': b'zza' },
            { 'mils':  766, 'expect': b'zzza' },
            { 'mils': 1021, 'expect': b'zzzza' },
        ]

        for test in tests:
            got = bytearray(self.object.make_distance( test['mils'] ))
            self.assertEqual( got, test['expect'] )

    def test_make_dir_dist(self):

        tests = [
            { 'x':  0, 'y':  0, 'expect': b'' },
            { 'x':  0, 'y':  1, 'expect': b'La' },       # Left
            { 'x':  0, 'y': -1, 'expect': b'Ra' },       # Right
            { 'x':  1, 'y':  0, 'expect': b'Ba' },       # Bottom
            { 'x': -1, 'y':  0, 'expect': b'Ta' },       # Top
        ]

        # make_dir_dist() is an up/down then left/right mover
        # TODO - test with laser_on=True (perhaps in test_move)

        for test in tests:
            self.data = bytearray()
            self.object.make_dir_dist( test['x'], test['y'] )
            self.object.flush()
            self.assertEqual( self.data, test['expect'] )

    def test_make_cut_line(self):
        with self.assertRaises(K40Exception):
            self.object.make_cut_line(1.5,1,Spindle=True)
        with self.assertRaises(K40Exception):
            self.object.make_cut_line(1,1.5,Spindle=True)

        tests = [
            { 'x':  0, 'y':  0, 'expect': b'D' },
            { 'x':  0, 'y':  1, 'expect': b'La' },
            { 'x':  0, 'y': -1, 'expect': b'Ra' },
            { 'x':  1, 'y':  0, 'expect': b'Ba' },
            { 'x': -1, 'y':  0, 'expect': b'Ta' },
            { 'x': 10, 'y': 10, 'expect': b'BLMj' },
            { 'x':  1, 'y':  1, 'expect': b'Ma' },
            { 'x': -1, 'y': -1, 'expect': b'TRMa' },
            { 'x': 16, 'y':  9, 'expect': b'BLMaBaMaBaMaBaMbBaMaBaMaBaMaBaMa' },
            { 'x': -9, 'y': 16, 'expect': b'TMaLaMaLaMaLaMbLaMaLaMaLaMaLaMa' },
            { 'x': 100, 'y': 7, 'expect': b'BgMaBmMaBmMaBnMaBmMaBmMaBmMaBg' },
        ]

        for test in tests:
            self.data = bytearray()
            self.object.make_cut_line( test['x'], test['y'], Spindle=True )
            self.object.flush()
            self.assertEqual( self.data, test['expect'] )

    def test_make_speed(self):
        with self.assertRaises(TypeError):
            self.object.make_speed()
        with self.assertRaises(K40Exception):
            self.object.make_speed(board_name='larry')
        with self.assertRaises(ZeroDivisionError):
            self.object.make_speed(Feed=0)

        tests = [
            { 'f':   1, 'b': 'LASER-M2', 's': 0, 'e': b'CV1551931001052089C' },
            { 'f':   6, 'b': 'LASER-M2', 's': 0, 'e': b'CV2390681004002046C' },
            { 'f':   7, 'b': 'LASER-M2', 's': 0, 'e': b'CV0640541004001222' },
            { 'f': 100, 'b': 'LASER-M2', 's': 0, 'e': b'CV2232481051000031' },
            { 'f': 100, 'b': 'LASER-M2', 's': 1, 'e': b'V2232481G001' },
            { 'f': 100, 'b': 'LASER-M2', 's': 9, 'e': b'V2232481G009' },

            { 'f':   1, 'b': 'LASER-M1', 's': 1, 'e': b'V167762491201G001' },
            { 'f':   6, 'b': 'LASER-M1', 's': 1, 'e': b'V0351471G001' },
            { 'f':   6, 'b': 'LASER-M1', 's': 0, 'e': b'CV0351471000000000' },

            { 'f':   1, 'b': 'LASER-M',  's': 1, 'e': b'V167762491201G001' },
            { 'f':   6, 'b': 'LASER-M',  's': 1, 'e': b'V0351471G001' },
            { 'f':   6, 'b': 'LASER-M',  's': 0, 'e': b'CV0351471' },

            { 'f': 0.7, 'b': 'LASER-B2', 's': 1, 'e': b'V167771821591G001C' },
            { 'f':   6, 'b': 'LASER-B2', 's': 1, 'e': b'V2191371G001C' },
            { 'f':   9, 'b': 'LASER-B2', 's': 1, 'e': b'V167772011811G001' },
            { 'f':  10, 'b': 'LASER-B2', 's': 1, 'e': b'V0121131G001' },
            { 'f':  10, 'b': 'LASER-B2', 's': 0, 'e': b'CV0121131000000000' },

            { 'f': 0.7, 'b': 'LASER-B1', 's': 0, 'e': b'CV167771851161000000000' },
            { 'f':   1, 'b': 'LASER-B1', 's': 0, 'e': b'CV0541281000000000' },
            { 'f':  10, 'b': 'LASER-B1', 's': 0, 'e': b'CV2330241000000000' },
            { 'f': 100, 'b': 'LASER-B1', 's': 0, 'e': b'CV2502431000000000' },
            { 'f': 100, 'b': 'LASER-B1', 's': 1, 'e': b'V2502431G001' },
            { 'f': 100, 'b': 'LASER-B1', 's': 9, 'e': b'V2502431G009' },

            { 'f': 0.7, 'b': 'LASER-A',  's': 1, 'e': b'V167771851161G001' },
            { 'f':   1, 'b': 'LASER-A',  's': 1, 'e': b'V0541281G001' },
            { 'f':   1, 'b': 'LASER-A',  's': 0, 'e': b'CV0541281' },

            { 'f': 0.7, 'b': 'LASER-B',  's': 1, 'e': b'V167771851161G001' },
        ]

        for test in tests:
            data = bytearray(self.object.make_speed(
                    Feed=test['f'],
                    board_name=test['b'],
                    Raster_step=test['s']
                ))
            self.assertEqual( data, test['e'] )


    def test_make_move_data(self):

        tests = [
            { 'x': 0, 'y': 0, 'expect': b'' },
            { 'x': 1, 'y': 1, 'expect': b'ILaBaS1P' },
            { 'x': 1000, 'y': 1000, 'expect': b'ILzzz235Bzzz235S1P' },
        ]

        # make_move_data() is essentially a wrapper around make_distance():
        # "I" "L{}" "B{}" "S1P", with the two {} filled in by make_distance

        for test in tests:
            self.data = bytearray()
            self.object.make_move_data( test['x'], test['y'] )
            self.assertEqual( self.data, test['expect'] )

    def test_ecoord_adj(self):

        tests = [
            { 'adj': [0,0,0],  'scale': 0, 'flip': 0, 'expect': (0,0,0) },
            { 'adj': [0,0,10], 'scale': 1, 'flip': 0, 'expect': (0,0,10) },
            { 'adj': [0,0,10], 'scale': 2, 'flip': 0, 'expect': (0,0,10) },
            { 'adj': [0,10,0], 'scale': 1, 'flip': 0, 'expect': (0,10,0) },
            { 'adj': [0,10,0], 'scale': 2, 'flip': 0, 'expect': (0,20,0) },
            { 'adj': [10,0,0], 'scale': 1, 'flip': 0, 'expect': (10,0,0) },
            { 'adj': [10,0,0], 'scale': 2, 'flip': 0, 'expect': (20,0,0) },
            { 'adj': [10,0,0], 'scale': 2, 'flip': 4, 'expect': (-12,0,0) },
        ]

        for test in tests:
            got = self.object.ecoord_adj(
                ecoords_adj_in=test['adj'],
                scale=test['scale'],
                FlipXoffset=test['flip']
            )
            self.assertEqual( got, test['expect'] )

    def test_make_egv_data(self):

        tests = [
            {
                'param': {
                    'ecoords_in': [[0,0,0],[0,0,0]], 'Feed': 1,
                },
                'expect': b'ICV1551931001052089CNRBS1EFNSE',
            },
            {
                'param': {
                    'ecoords_in': [[0,0,0],[0,0,0]], 'Feed': 1,
                    'startX': 0.01, 'startY': 0.02,
                },
                'expect': b'ICV1551931001052089CRtTjNRBS1ETcLcTNLqBmSEFNSE',
            },
            {
                'param': {
                    'ecoords_in': [[0,0,0],[0,0,0]], 'Feed': 1,
                    'units': 'mm',
                    'startX': 0.2, 'startY': 0.4,
                },
                'expect': b'ICV1551931001052089CRpThNRBS1ETcLcTNLmBkSEFNSE',
            },
            {
                'param': {
                    'ecoords_in': [[0,0,0],[0.1,0,1],[0.1,0.1,0],[0,0.1,1]],
                    'Feed': 1,
                },
                'expect': b'ICV1551931001052089CNRBS1ETcLcTNRcB103SETcLcTNL097BcSETcLcBNRcT097SETcLcTNR103BcSEFNSE',
            },
            {
                'param': {
                    'ecoords_in': [[0,0,1],[0.1,0,1],[0.1,0.1,0],[0,0.1,0]],
                    'Feed': 1,
                },
                'expect': b'ICV1551931001052089CNRBS1EDB100UTcLcTNL097BcSEDT100UTcLcTNR103BcSEFNSE',
            },
            {
                'param': {
                    'ecoords_in': [[0,0,1],[0.004,0,1],[0.004,0.004,0],[0,0.004,0]],
                    'Feed': 1,
                },
                'expect': b'ICV1551931001052089CNRBS1EDBdULdDTdURdFNSE',
            },

            # test the variable feed speed
            {
                'param': {
                    'ecoords_in': [[0,0,0,0.5],[0,0,0]], 'Feed': None,
                },
                'expect': b'ICV167769941981001252487CNRBS1EFNSE',
            },
            {
                'param': {
                    'ecoords_in': [[0,0,0,0.2],[0,0,0]], 'Feed': None,
                },
                'expect': b'ICV1677621908510011046633CNRBS1EFNSE',
            },
            {
                # Test varing the feed speed during a cut
                'param': {
                    'ecoords_in': [
                        [0,0,1,0.2,1],
                        [0.004,0,1,0.2,1],
                        [0.004,0.004,0,0.2,1],
                        [0,0.004,0,0.5,1]
                    ],
                    'Feed': None,
                },
                'expect': b'ICV1677621908510011046633CNRBS1EDBdULdUReTe@NSECV167769941981001252487CNRBS1ELeBeDDTdURdFNSE',
            },

            # TODO
            # - big enough movement to get rapid_move_fast
            # - laser on
            # - laser on and variable_fee/
        ]

        # TODO
        # - raster

        for test in tests:
            self.data = bytearray()
            self.object.make_egv_data(**test['param'])
            self.assertEqual( self.data, test['expect'] )

# TODO
# - test_rapid_move_fast
#       (currently covers everything but a strange padding test)
# - test_change_speed
#       (currently covers everything except case where laser_on==false)

