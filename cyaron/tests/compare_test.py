import unittest
import os
import shutil
import tempfile
from cyaron import IO, Compare
from cyaron.output_capture import captured_output

class TestCompare(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        os.chdir(self.temp_directory)

    def tearDown(self):
        shutil.rmtree(self.temp_directory)

    def test_noipstyle_correct(self):
        io = None
        with captured_output() as (out, err):
            io = IO("test_compare.in", "test_compare.out")

        io.output_writeln("test123 \ntest123\n")
        with open("test_another.out", "w") as f:
            f.write("test123\r\ntest123 ")

        with captured_output() as (out, err):
            Compare.output("test_another.out", std=io)

        result = out.getvalue().strip()
        self.assertEqual(result, "test_another.out: Correct")

    def test_noipstyle_incorrect(self):
        io = None
        with captured_output() as (out, err):
            io = IO("test_compare_incorrect.in", "test_compare_incorrect.out")

        io.output_writeln("test123 \ntest123\n")
        with open("test_another_incorrect.out", "w") as f:
            f.write("test123\r\ntest124 ")

        with captured_output() as (out, err):
            Compare.output("test_another_incorrect.out", std=io)

        result = out.getvalue().strip()
        self.assertEqual(result, "test_another_incorrect.out: !!!INCORRECT!!! On line 2 column 7, read 4, expected 3.")