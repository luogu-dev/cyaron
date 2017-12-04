from __future__ import absolute_import
from .utils import *
from . import log
from io import open, IOBase
import subprocess
import tempfile
import os
import re


class IO(object):
    """Class IO: IO tool class. It will process the input and output files."""
    def __init__(self, input_file=None, output_file=None, data_id=None, file_prefix=None, input_suffix='.in', output_suffix='.out', disable_output=False):
        """__init__(self, input_file=None, output_file=None, data_id=None, file_prefix=None, input_suffix='.in', output_suffix='.out', disable_output=False) -> None
            input_file, output_file overload:
                None -> make a temp file (if file_prefix is None)
                file object -> treat the file-like object as in/output file
                int -> open file by file descriptor
                str -> a filename or filename template like 'awd{}.in'. ``{}`` will be replaced by ``data_id``
            int data_id -> the id of the data. if it's None, the file names will not contain the id.
            legacy argumants:
                str file_prefix -> the prefix for the input and output files
                str input_suffix = ".in" -> the suffix of the input file
                str output_suffix = ".out" -> the suffix of the output file
            disable_output -> bool, set to True to disable output
            Examples:
                IO("a","b") -> create input file "a" and output file "b"
                IO("a.in","b.out") -> create input file "a.in" and output file "b.out"
                IO(file_prefix="data") -> create input file "data.in" and output file "data.out"
                IO(file_prefix="data",data_id=1) -> create input file "data1.in" and output file "data1.out"
                IO(file_prefix="data",input_suffix=".input") -> create input file "data.input" and output file "data.out"
                IO(file_prefix="data",output_suffix=".output") -> create input file "data.in" and output file "data.output"
                IO(file_prefix="data",data_id=2,input_suffix=".input") -> create input file "data2.input" and output file "data2.out"
                IO("data{}.in","data{}.out",data_id=2) -> create input file "data2.in" and output file "data2.out"
                IO(open('data.in', 'w+'), open('data.out', 'w+')) -> input file "data.in" and output file "data.out"
        """
        if file_prefix is not None:
            # legacy mode
            input_file = '{}{{}}{}'.format(self.__escape_format(file_prefix), self.__escape_format(input_suffix))
            output_file = '{}{{}}{}'.format(self.__escape_format(file_prefix), self.__escape_format(output_suffix))
        self.input_filename, self.output_filename = None, None
        self.__input_temp, self.__output_temp = False, False
        self.__init_file(input_file, data_id, 'i')
        if not disable_output:
            self.__init_file(output_file, data_id, 'o')
        else:
            self.output_file = None
        self.__closed = False
        self.is_first_char = {}

    def __init_file(self, f, data_id, file_type):
        try:
            is_file = isinstance(f, file)
        except NameError:
            is_file = False
        if isinstance(f, IOBase) or is_file:
            # consider ``f`` as a file object
            if file_type == 'i':
                self.input_file = f
            else:
                self.output_file = f
        elif isinstance(f, int):
            # consider ``f`` as a file descor
            self.__init_file(open(f, 'w+', newline='\n'), data_id, file_type)
        elif f is None:
            # consider wanna temp file
            fd, self.input_filename = tempfile.mkstemp()
            self.__init_file(fd, data_id, file_type)
            if file_type == 'i':
                self.__input_temp = True
            else:
                self.__output_temp = True
        else:
            # consider ``f`` as filename template
            filename = f.format(data_id)
            if file_type == 'i':
                self.input_filename = filename
                log.debug("Processing %s" % self.input_filename)
            else:
                self.output_filename = filename
            self.__init_file(open(filename, 'w+', newline='\n'), data_id, file_type)

    def __escape_format(self, st):
        """replace "{}" to "{{}}" """
        return re.sub(r'\{', '{{', re.sub(r'\}', '}}', st))

    def __del_files(self):
        """delete files"""
        if self.__input_temp and self.input_filename is not None:
            os.remove(self.input_filename)
        if self.__output_temp and self.output_filename is not None:
            os.remove(self.output_filename)

    def close(self):
        """Delete the IO object and close the input file and the output file"""
        if self.__closed:
            # avoid double close
            return
        deleted = False
        try:
            # on posix, one can remove a file while it's opend by a process
            # the file then will be not visable to others, but process still have the file descriptor
            # it is recommand to remove temp file before close it on posix to avoid race
            # on nt, it will just fail and raise OSError so that after closing remove it again
            self.__del_files()
            deleted = True
        except OSError:
            pass
        if isinstance(self.input_file, IOBase):
            self.input_file.close()
        if isinstance(self.output_file, IOBase):
            self.output_file.close()
        if not deleted:
            self.__del_files()
        self.__closed = True

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
        self.flush_buffer()
        origin_pos = self.input_file.tell()
        self.input_file.seek(0)
        subprocess.check_call(shell_cmd, shell=True, stdin=self.input_file, stdout=self.output_file, universal_newlines=True)
        self.input_file.seek(origin_pos)

        log.debug(self.output_filename, " done")

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
