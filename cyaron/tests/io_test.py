import unittest
import os
import shutil
import tempfile
from cyaron import IO
from cyaron.output_capture import captured_output


class TestIO(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        os.chdir(self.temp_directory)

    def tearDown(self):
        try:
            shutil.rmtree(self.temp_directory)
        except:
            pass

    def test_create_files_simple(self):
        with captured_output() as (out, err):
            IO("test_simple.in", "test_simple.out")
        self.assertTrue(os.path.exists("test_simple.in"))
        self.assertTrue(os.path.exists("test_simple.out"))

    def test_create_files_prefix_id(self):
        with captured_output() as (out, err):
            IO(file_prefix="test_prefix", data_id=233, input_suffix=".inp", output_suffix=".ans")
        self.assertTrue(os.path.exists("test_prefix233.inp"))
        self.assertTrue(os.path.exists("test_prefix233.ans"))

    def test_write_stuff(self):
        with captured_output() as (out, err):
            with IO("test_write.in", "test_write.out") as test:
                test.input_write(1, 2, 3)
                test.input_writeln([4, 5, 6])
                test.input_writeln(7, [8, 9])
                test.output_write([9, 8], 7)
                test.output_writeln(6, 5, 4)
                test.output_writeln([3], 2, [1])

        with open("test_write.in") as f:
            input = f.read()
        with open("test_write.out") as f:
            output = f.read()
        self.assertEqual(input.split(), ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.assertEqual(output.split(), ['9', '8', '7', '6', '5', '4', '3', '2', '1'])
        self.assertEqual(input.count("\n"), 2)
        self.assertEqual(output.count("\n"), 2)

    def test_output_gen(self):
        with captured_output() as (out, err):
            with IO("test_gen.in", "test_gen.out") as test:
                test.output_gen("echo 233")

        with open("test_gen.out") as f:
            output = f.read()
        self.assertEqual(output.strip("\n"), "233")