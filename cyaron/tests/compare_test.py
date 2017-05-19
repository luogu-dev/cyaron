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
        try:
            shutil.rmtree(self.temp_directory)
        except:
            pass

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

    def test_fulltext_program(self):
        with open("correct.py", "w") as f:
            f.write("print(1)")

        with open("incorrect.py", "w") as f:
            f.write("print(2)")

        io = None
        with captured_output() as (out, err):
            io = IO("test_fulltext.in", "test_fulltext.out")

        io.output_writeln("1")

        with captured_output() as (out, err):
            Compare.program("python correct.py", "python incorrect.py", std=io, input=io, grader="FullText")

        result = out.getvalue().strip()
        correct_text = 'python correct.py: Correct \npython incorrect.py: !!!INCORRECT!!! Hash mismatch: read 53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3, expected 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'
        self.assertEqual(result, correct_text)

