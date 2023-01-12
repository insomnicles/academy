import unittest
from click.testing import CliRunner
from convert_gutenberg import convert_gutenberg

# 0, None: Success
# 1: Error
# 2: Command line syntax errors
# 120: Error during process cleanup.
# 255: Exit code out of range.

class TestCmdlineInvalid(unittest.TestCase):

    def test_no_arguments(self):
        runner = CliRunner()
        result = runner.invoke(convert_gutenberg, [ ])
        self.assertEqual(result.exit_code, 2)

    def test_three_missing_argument(self):
        runner = CliRunner()
        result = runner.invoke(convert_gutenberg, [ "1323", "easy" ])
        self.assertEqual(result.exit_code, 2)

    def test_two_missing_argument(self):
        runner = CliRunner()
        result = runner.invoke(convert_gutenberg, [ "1323", "html", "easy" ])
        self.assertEqual(result.exit_code, 2)

    def test_one_missing_argument(self):
        runner = CliRunner()
        result = runner.invoke(convert_gutenberg, [ "output/tests", "html", "easy" ])
        self.assertEqual(result.exit_code, 2)
        
    def test_invalid_option(self):
        runner = CliRunner()
        result = runner.invoke(convert_gutenberg, [ "1323", "html", "output/tests", "easy", "--savesrc", "--asdfasdfasdf" ])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual("No such option" in result.output, True)
    
    def test_id_html_easy_no_options(self):
        runner = CliRunner()
        result = runner.invoke(convert_gutenberg, [ "1323", "html", "output/tests", "easy" ])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual("Successful" in result.output, True)
