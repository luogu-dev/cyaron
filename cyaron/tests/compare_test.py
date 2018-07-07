import unittest
import os
import sys
import shutil
import tempfile
import subprocess
from cyaron import IO, Compare, log
from cyaron.output_capture import captured_output
from cyaron.graders.mismatch import *
from cyaron.compare import CompareMismatch

log.set_verbose()

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

        try:
            with captured_output() as (out, err):
                Compare.output("test_another_incorrect.out", std=io)
        except CompareMismatch as e:
            self.assertEqual(e.name, 'test_another_incorrect.out')
            e = e.mismatch
            self.assertEqual(e.content, 'test123\r\ntest124 ')
            self.assertEqual(e.std, 'test123 \ntest123\n\n')
            self.assertEqual(str(e), 'On line 2 column 7, read 4, expected 3.')
        else:
            self.assertTrue(False)

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

        try:
            with captured_output() as (out, err):
                Compare.program("python correct.py", "python incorrect.py", std=io, input=io, grader="FullText")
        except CompareMismatch as e:
            self.assertEqual(e.name, 'python incorrect.py')
            e = e.mismatch
            self.assertEqual(e.content, '2\n')
            self.assertEqual(e.std, '1\n')
            self.assertEqual(e.content_hash, '53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3')
            self.assertEqual(e.std_hash, '4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865')
        else:
            self.assertTrue(False)

        result = out.getvalue().strip()
        correct_out = 'python correct.py: Correct \npython incorrect.py: !!!INCORRECT!!! Hash mismatch: read 53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3, expected 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'
        self.assertEqual(result, correct_out)

    def test_file_input(self):
        with open("correct.py", "w") as f:
            f.write("print(input())")

        with open("std.py", "w") as f:
            f.write("print(input())")

        io = None
        with captured_output() as (out, err):
            io = IO()

        io.input_writeln("233")

        with captured_output() as (out, err):
            Compare.program("python correct.py", std_program="python std.py", input=io, grader="NOIPStyle")

        result = out.getvalue().strip()
        correct_out = 'python correct.py: Correct'
        self.assertEqual(result, correct_out)

    def test_concurrent(self):
        programs = ['test{}.py'.format(i) for i in range(16)]
        for fn in programs:
            with open(fn, 'w') as f:
                f.write('print({})'.format(16))
        with open('std.py', 'w') as f:
            f.write('print({})'.format(16))
        with IO() as test:
            Compare.program(*[(sys.executable, program) for program in programs], std_program=(sys.executable, 'std.py'), max_workers=None, input=test)

        ios = [IO() for i in range(16)]
        try:
            for f in ios:
                f.output_write('16')
            with IO() as std:
                std.output_write('16')
                Compare.output(*ios, std=std, max_workers=None)
        finally:
            for io in ios:
                io.close()

    def test_timeout(self):
        if sys.version_info >= (3, 3):
            with IO() as test:
                try:
                    Compare.program(((sys.executable, '-c', '__import__(\'time\').sleep(10)'), 1), std=test, input=test)
                except subprocess.TimeoutExpired:
                    pass
                else:
                    self.assertTrue(False)
