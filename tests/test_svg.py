#
# Let's at least try not to break it, ok?
#

import unittest
import os
import json

from k40.svg import SVGReader

class TestSVGReader(unittest.TestCase):
    def test_file1(self):
        self.run_file_test('tests/data/test1.svg')

    def test_file2(self):
        self.run_file_test('tests/data/test2.svg')

    def run_file_test(self, filename, reference=None):
        if reference is None:
            reference = filename + '.json'

        reader = SVGReader()
        reader.image_dpi = 1000

        # FIXME: this is required
        reader.set_inkscape_path("")

        reader.parse(filename)
        reader.make_paths()

        dump = {
            'cut_lines': reader.cut_lines,
            'eng_lines': reader.eng_lines,
            'xsize': reader.Xsize,
            'ysize': reader.Ysize,
            }

        if not os.path.isfile(reference):
            # Initial build
            with open(reference, 'w+') as fd:
                json.dump(dump, fd)
            return

        with open(reference) as fd:
            ref_dump = json.load(fd)
            for k, v in ref_dump.items():
                self.assertEqual(v, dump[k], k)
