from __future__ import absolute_import
from .utils import *
from io import open
import subprocess
import tempfile
import os


class IO(object):
    """Class IO: IO tool class. It will process the input and output files."""
    def __init__(self, *args, **kwargs):
        """__init__(self, *args, **kwargs) -> None
            (str,str) args -> The file names of input file and output file. Index 0 is the name of input file, and index 1 is for output file
            **kwargs:
                str file_prefix -> the prefix for the input and output files
                int data_id -> the id of the data. if it's None, the file names will not contain the id.
                str input_suffix = ".in" -> the suffix of the input file
                str output_suffix = ".out" -> the suffix of the output file
            Examples:
                IO("a","b") -> create input file "a" and output file "b"
                IO("a.in","b.out") -> create input file "a.in" and output file "b.out"
                IO(file_prefix="data") -> create input file "data.in" and output file "data.out"
                IO(file_prefix="data",data_id=1) -> create input file "data1.in" and output file "data1.out"
                IO(file_prefix="data",input_suffix=".input") -> create input file "data.input" and output file "data.out"
                IO(file_prefix="data",output_suffix=".output") -> create input file "data.in" and output file "data.output"
                IO(file_prefix="data",data_id=2,input_suffix=".input") -> create input file "data2.input" and output file "data2.out"
        """
        if len(args) == 0:
            if not "file_prefix" in kwargs:
                self.file_flag = 0
                (fd, self.input_filename) = tempfile.mkstemp()
                os.close(fd)
                (fd, self.output_filename) = tempfile.mkstemp()
                os.close(fd)
            else:
                self.file_flag = 2
                if "data_id" in kwargs:
                    filename_prefix = "%s%d" % (kwargs["file_prefix"], kwargs["data_id"])
                else:
                    filename_prefix = kwargs["file_prefix"]

                input_suffix = kwargs.get("input_suffix", ".in")
                output_suffix = kwargs.get("output_suffix", ".out")
                disable_output = kwargs.get("disable_output", False)
                self.input_filename = filename_prefix + input_suffix
                self.output_filename = filename_prefix + output_suffix if not disable_output else None
        elif len(args) == 1:
            self.file_flag = 1
            self.input_filename = args[0]
            (fd, self.output_filename) = tempfile.mkstemp()
            os.close(fd)
        elif len(args) == 2:
            self.file_flag = 2
            self.input_filename = args[0]
            self.output_filename = args[1]
        else:
            raise Exception("Invalid argument count")

        self.input_file = open(self.input_filename, 'w+', newline='\n')
        self.output_file = open(self.output_filename, 'w+', newline='\n') if self.output_filename else None
        self.is_first_char = dict()
        if self.file_flag != 0:
            print("Processing %s" % self.input_filename)

    def __del__(self):
        """__del__(self) -> None
            Delete the IO object and close the input file and the output file
        """
        try:
            self.input_file.close()
            self.output_file.close()
            if self.file_flag <= 1:
                os.remove(self.output_filename)
            if self.file_flag == 0:
                os.remove(self.input_filename)
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """__del__(self) -> None
            Exit the context of the IO object and close the input file and the output file
        """
        try:
            self.input_file.close()
            self.output_file.close()
            if self.file_flag <= 1:
                os.remove(self.output_filename)
            if self.file_flag == 0:
                os.remove(self.input_filename)
        except Exception:
            pass

    def __write(self, file, *args, **kwargs):
        """__write(self, file, *args, **kwargs) -> None
            Write every element in *args into file. If the element isn't "\n", insert a space. It will convert every element into str
            file file -> the file object to write
            **kwargs:
                str separator = " " -> a string used to separate every element
        """
        separator = kwargs.get("separator", " ")
        for arg in args:
            if list_like(arg):
                self.__write(file, *arg, **kwargs)
            else:
                if arg != "\n" and not self.is_first_char.get(file, True):
                    file.write(make_unicode(separator))
                self.is_first_char[file] = False
                file.write(make_unicode(arg))
                if arg == "\n":
                    self.is_first_char[file] = True

    def input_write(self, *args, **kwargs):
        """input_write(self, *args, **kwargs) -> None
            Write every element in *args into the input file. Splits with spaces. It will convert every element into string
            **kwargs:
                str separator = " " -> a string used to separate every element
        """
        self.__write(self.input_file, *args, **kwargs)

    def input_writeln(self, *args, **kwargs):
        """input_writeln(self, *args, **kwargs) -> None
            Write every element in *args into the input file and turn to a new line. Splits with spaces. It will convert every element into string
            **kwargs:
                str separator = " " -> a string used to separate every element
        """
        args = list(args)
        args.append("\n")
        self.input_write(*args, **kwargs)

    def output_gen(self, shell_cmd):
        """output_gen(self, shell_cmd) -> None
            Run the command shell_cmd(usually the std programme) and send it the input file as stdin. Write its output to the output file.
            str shell_cmd -> the command to run, usually the std programme
        """
        self.input_file.close()
        with open(self.input_filename, 'r') as f:
            self.output_file.write(make_unicode(subprocess.check_output(shell_cmd, shell=True, stdin=f, universal_newlines=True)))

        self.input_file = open(self.input_filename, 'a+')
        print(self.output_filename, " done")

    def output_write(self, *args, **kwargs):
        """output_write(self, *args, **kwargs) -> None
            Write every element in *args into the output file. Splits with spaces. It will convert every element into string
            **kwargs:
                str separator = " " -> a string used to separate every element
        """
        self.__write(self.output_file, *args, **kwargs)

    def output_writeln(self, *args, **kwargs):
        """output_writeln(self, *args, **kwargs) -> None
            Write every element in *args into the output file and turn to a new line. Splits with spaces. It will convert every element into string
            **kwargs:
                str separator = " " -> a string used to separate every element
        """
        args = list(args)
        args.append("\n")
        self.output_write(*args, **kwargs)

    def flush_buffer(self):
        self.input_file.flush()
