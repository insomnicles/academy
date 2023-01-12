import unittest
from click.testing import CliRunner

from convert_gutenberg import convert_gutenberg
from convert_gutenberg import BeautifyGutenberg

class TestBeautifyGutenberg(unittest.TestCase):

    def test_convert_html_from_url(self):
        bg = BeautifyGutenberg("html", 'easy', True, True)
        expected = 'output/tests/pg1323-images.html'
        actual = bg.convertFromUrl(1323, "output/tests")
        self.assertEqual(expected, actual)

    def test_convert_epub_from_url(self):
        bg = BeautifyGutenberg("epub", "easy", True, True)
        expected = 'output/tests/pg1323.epub'
        actual = bg.convertFromUrl(1323, "output/tests")
        self.assertEqual(expected, actual)

    # def test_convert_from_local(self):
    #     bg = BeautifyGutenberg("html", "easy", True, True)
    #     expected='output/tests/pg1323-images.html'
    #     actual=bg.convertFromLocal(1323, "output/tests")
    #     self.assertEqual(expected, actual)

    # def test_convert_all_local(self):
    #     bg = BeautifyGutenberg("html", "easy", True, True)
    #     expected = "output/tests/pg1323-images.html"
    #     actual = bg.convertFromAllLocal("../example", "output/tests")
    #     self.assertEqual(expected, actual)
    #     # self.assertEqual("Successful" in result.output, True)

if __name__ == '__main__':
    unittest.main()

