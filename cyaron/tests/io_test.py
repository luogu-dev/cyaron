import unittest
import sys
import os
import time
import shutil
import tempfile
import subprocess
from cyaron import IO
from cyaron.output_capture import captured_output


class TestIO(unittest.TestCase):

    def setUp(self):
        self.original_directory = os.getcwd()
        self.temp_directory = tempfile.mkdtemp()
        os.chdir(self.temp_directory)

    def tearDown(self):
        os.chdir(self.original_directory)
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
            IO(
                file_prefix="test_prefix",
                data_id=233,
                input_suffix=".inp",
                output_suffix=".ans",
            )
        self.assertTrue(os.path.exists("test_prefix233.inp"))
        self.assertTrue(os.path.exists("test_prefix233.ans"))

    def test_create_files_without_prefix_id(self):
        with captured_output() as (out, err):
            IO(file_prefix="test_prefix")
        self.assertTrue(os.path.exists("test_prefix.in"))
        self.assertTrue(os.path.exists("test_prefix.out"))

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
        self.assertEqual(input.split(),
                         ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.assertEqual(output.split(),
                         ["9", "8", "7", "6", "5", "4", "3", "2", "1"])
        self.assertEqual(input.count("\n"), 2)
        self.assertEqual(output.count("\n"), 2)

    def test_output_gen(self):
        with captured_output() as (out, err):
            with IO("test_gen.in", "test_gen.out") as test:
                test.output_gen("echo 233")

        with open("test_gen.out", "rb") as f:
            output = f.read()
        self.assertEqual(output, b"233\n")

    def test_output_gen_time_limit_exceeded(self):
        with captured_output():
            TIMEOUT = 0.02
            WAIT_TIME = 0.4  # If the wait time is too short, an error may occur
            with open("long_time.py", "w", encoding="utf-8") as f:
                f.write("import time, os\n"
                        "fn = input()\n"
                        f"time.sleep({WAIT_TIME})\n"
                        "os.remove(fn)\n")

            with IO("test_gen.in", "test_gen.out") as test:
                fd, input_filename = tempfile.mkstemp()
                os.close(fd)
                abs_input_filename: str = os.path.abspath(input_filename)
                with self.assertRaises(subprocess.TimeoutExpired):
                    test.input_writeln(abs_input_filename)
                    test.output_gen(f'"{sys.executable}" long_time.py',
                                    time_limit=TIMEOUT)
                time.sleep(WAIT_TIME)
                try:
                    os.remove(input_filename)
                except FileNotFoundError:
                    self.fail("Child processes have not been terminated.")

    def test_output_gen_time_limit_not_exceeded(self):
        with captured_output():
            with open("short_time.py", "w", encoding="utf-8") as f:
                f.write("import time\n"
                        "time.sleep(0.1)\n"
                        "print(1)")

            with IO("test_gen.in", "test_gen.out") as test:
                test.output_gen(f'"{sys.executable}" short_time.py',
                                time_limit=0.5)
        with open("test_gen.out", encoding="utf-8") as f:
            output = f.read()
        self.assertEqual(output, "1\n")

    def test_init_overload(self):
        with IO(file_prefix="data{", data_id=5) as test:
            self.assertEqual(test.input_filename, "data{5.in")
            self.assertEqual(test.output_filename, "data{5.out")
        with IO("data{}.in", "data{}.out", 5) as test:
            self.assertEqual(test.input_filename, "data5.in")
            self.assertEqual(test.output_filename, "data5.out")
        with open("data5.in", "w+") as fin:
            with open("data5.out", "w+") as fout:
                with IO(fin, fout) as test:
                    self.assertEqual(test.input_file, fin)
                    self.assertEqual(test.output_file, fout)

    def test_make_dirs(self):
        mkdir_true = False
        with IO("./automkdir_true/data.in",
                "./automkdir_true/data.out",
                make_dirs=True):
            mkdir_true = os.path.exists("./automkdir_true")
        self.assertEqual(mkdir_true, True)

        mkdir_false = False
        try:
            with IO("./automkdir_false/data.in", "./automkdir_false/data.out"):
                pass
        except FileNotFoundError:
            mkdir_false = True
        mkdir_false &= not os.path.exists("./automkdir_false")
        self.assertEqual(mkdir_false, True)

    def test_output_clear_content(self):
        with IO("test_clear.in", "test_clear.out") as test:
            test.input_write("This is a test.")
            test.input_clear_content()
            test.input_write("Cleared content.")
            test.output_write("This is a test.")
            test.output_clear_content()
            test.output_write("Cleared content.")
        with open("test_clear.in", encoding="utf-8") as f:
            input_text = f.read()
        with open("test_clear.out", encoding="utf-8") as f:
            output_text = f.read()
        self.assertEqual(input_text, "Cleared content.")
        self.assertEqual(output_text, "Cleared content.")

    def test_output_clear_content_with_position(self):
        with IO("test_clear_pos.in", "test_clear_pos.out") as test:
            test.input_write("This is a test.")
            test.input_clear_content(5)
            test.input_write("Cleared content.")
            test.output_write("This is a test.")
            test.output_clear_content(5)
            test.output_write("Cleared content.")
        with open("test_clear_pos.in", encoding="utf-8") as f:
            input_text = f.read()
        with open("test_clear_pos.out", encoding="utf-8") as f:
            output_text = f.read()
        self.assertEqual(input_text, "This Cleared content.")
        self.assertEqual(output_text, "This Cleared content.")
