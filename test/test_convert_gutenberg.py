import unittest
from click.testing import CliRunner

from convert_gutenberg import convert_gutenberg
from convert_gutenberg import BeautifyGutenberg

class TestBeautifyGutenberg(unittest.TestCase):

    # basic dialogue
    def test_convert_gutenberg(self):
        bg = BeautifyGutenberg()
        expected='output/tests/pg1323-images.html'
        actual=bg.convertFromUrl(1323, "output/tests", "easy", True, True)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

