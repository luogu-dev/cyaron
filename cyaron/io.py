"""
A module that provides a class IO to process the input and output files.
Classes:
    IO: IO tool class. It will process the input and output files.
"""

from __future__ import absolute_import
import os
import re
import signal
import subprocess
import tempfile
from typing import Union, overload, Optional, List, cast
from io import IOBase
from . import log
from .utils import list_like, make_unicode


class IO:
    """IO tool class. It will process the input and output files."""

    @overload
    def __init__(
        self,
        input_file: Optional[Union[IOBase, str, int]] = None,
        output_file: Optional[Union[IOBase, str, int]] = None,
        data_id: Optional[int] = None,
        disable_output: bool = False,
        make_dirs: bool = False,
    ):
        ...

    @overload
    def __init__(
        self,
        data_id: Optional[int] = None,
        file_prefix: Optional[str] = None,
        input_suffix: str = ".in",
        output_suffix: str = ".out",
        disable_output: bool = False,
        make_dirs: bool = False,
    ):
        ...

    def __init__(  # type: ignore
        self,
        input_file: Optional[Union[IOBase, str, int]] = None,
        output_file: Optional[Union[IOBase, str, int]] = None,
        data_id: Optional[int] = None,
        file_prefix: Optional[str] = None,
        input_suffix: str = ".in",
        output_suffix: str = ".out",
        disable_output: bool = False,
        make_dirs: bool = False,
    ):
        """
        Args:
            input_file (optional): input file object or filename or file descriptor.
                If it's None, make a temp file. Defaults to None.
            output_file (optional): input file object or filename or file descriptor.
                If it's None, make a temp file. Defaults to None.
            data_id (optional): the id of the data. It will be add after
                `input_file` and `output_file` when they are str.
                If it's None, the file names will not contain the id. Defaults to None.
            file_prefix (optional): the prefix for the input and output files. Defaults to None.
            input_suffix (optional): the suffix of the input file. Defaults to '.in'.
            output_suffix (optional): the suffix of the output file. Defaults to '.out'.
            disable_output (optional): set to True to disable output file. Defaults to False.
            make_dirs (optional): set to True to create dir if path is not found. Defaults to False.
        Examples:
            >>> IO("a","b")
            # create input file "a" and output file "b"
            >>> IO("a.in","b.out")
            # create input file "a.in" and output file "b.out"
            >>> IO(file_prefix="data")
            # create input file "data.in" and output file "data.out"
            >>> IO(file_prefix="data",data_id=1)
            # create input file "data1.in" and output file "data1.out"
            >>> IO(file_prefix="data",input_suffix=".input")
            # create input file "data.input" and output file "data.out"
            >>> IO(file_prefix="data",output_suffix=".output")
            # create input file "data.in" and output file "data.output"
            >>> IO(file_prefix="data",data_id=2,input_suffix=".input")
            # create input file "data2.input" and output file "data2.out"
            >>> IO("data{}.in","data{}.out",data_id=2)
            # create input file "data2.in" and output file "data2.out"
            >>> IO(open('data.in', 'w+'), open('data.out', 'w+'))
            # input file "data.in" and output file "data.out"
            >>> IO("./io/data.in", "./io/data.out", disable_output = True)
            # input file "./io/data.in" and output file "./io/data.out"
            # if the dir "./io" not found it will be created
        """
        self.__closed = False
        self.input_file = cast(IOBase, None)
        self.output_file = None
        if file_prefix is not None:
            # legacy mode
            input_file = "{}{{}}{}".format(self.__escape_format(file_prefix),
                                           self.__escape_format(input_suffix))
            output_file = "{}{{}}{}".format(
                self.__escape_format(file_prefix),
                self.__escape_format(output_suffix))
        self.input_filename, self.output_filename = None, None
        self.__input_temp, self.__output_temp = False, False
        self.__init_file(input_file, data_id, "i", make_dirs)
        if not disable_output:
            self.__init_file(output_file, data_id, "o", make_dirs)
        else:
            self.output_file = None
        self.is_first_char = {}

    def __init_file(
        self,
        f: Union[IOBase, str, int, None],
        data_id: Union[int, None],
        file_type: str,
        make_dirs: bool,
    ):
        if isinstance(f, IOBase):
            # consider ``f`` as a file object
            if file_type == "i":
                self.input_file = f
            else:
                self.output_file = f
        elif isinstance(f, int):
            # consider ``f`` as a file descor
            self.__init_file(
                open(f, "w+", encoding="utf-8", newline="\n"),
                data_id,
                file_type,
                make_dirs,
            )
        elif f is None:
            # consider wanna temp file
            fd, filename = tempfile.mkstemp()
            self.__init_file(fd, data_id, file_type, make_dirs)
            if file_type == "i":
                self.input_filename = filename
                self.__input_temp = True
            else:
                self.output_filename = filename
                self.__output_temp = True
        else:
            # consider ``f`` as filename template
            filename = f.format(data_id or "")
            # be sure dir is existed
            if make_dirs:
                self.__make_dirs(filename)
            if file_type == "i":
                self.input_filename = filename
            else:
                self.output_filename = filename
            self.__init_file(
                open(filename, "w+", newline="\n", encoding="utf-8"),
                data_id,
                file_type,
                make_dirs,
            )

    def __escape_format(self, st: str):
        """replace "{}" to "{{}}" """
        return re.sub(r"\{", "{{", re.sub(r"\}", "}}", st))

    def __make_dirs(self, pth: str):
        os.makedirs(os.path.dirname(pth), exist_ok=True)

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
            # the file then will be not visable to others,
            # but process still have the file descriptor
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

    def __write(self, file: IOBase, *args, **kwargs):
        """
        Write every element in *args into file. If the element isn't "\n", insert `separator`.
        It will convert every element into str.
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

    def __clear(self, file: IOBase, pos: int = 0):
        """
        Clear the content use truncate()
        Args:
            file: Which file to clear
            pos: Where file will truncate.
        """
        file.truncate(pos)
        self.is_first_char[file] = True
        file.seek(pos)

    @staticmethod
    def _kill_process_and_children(proc: subprocess.Popen):
        if os.name == "posix":
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        elif os.name == "nt":
            os.system(f"TASKKILL /F /T /PID {proc.pid} > nul")
        else:
            proc.kill()  # Not currently supported

    def input_write(self, *args, **kwargs):
        """
        Write every element in *args into the input file. Splits with `separator`.
        It will convert every element into str.
        Args:
            *args: the elements to write
            separator: a string used to separate every element. Defaults to " ".
        """
        self.__write(self.input_file, *args, **kwargs)

    def input_writeln(self, *args, **kwargs):
        """
        Write every element in *args into the input file and turn to a new line
        Splits with `separator`.
        It will convert every element into str.
        Args:
            *args: the elements to write
            separator: a string used to separate every element. Defaults to " ".
        """
        args = list(args)
        args.append("\n")
        self.input_write(*args, **kwargs)

    def input_clear_content(self, pos: int = 0):
        """
        Clear the content of input
        Args:
            pos: Where file will truncate.
        """

        self.__clear(self.input_file, pos)

    def output_gen(self,
                   shell_cmd: Union[str, List[str]],
                   time_limit: Optional[float] = None,
                   *,
                   replace_EOL: bool = True):
        """
        Run the command `shell_cmd` (usually the std program) and send it the input file as stdin.
        Write its output to the output file.
        Args:
            shell_cmd: the command to run, usually the std program.
            time_limit: the time limit (seconds) of the command to run.
                None means infinity. Defaults to None.
            replace_EOL: Set whether to replace the end-of-line sequence with `'\\n'`.
                Defaults to True.
        """
        if self.output_file is None:
            raise ValueError("Output file is disabled")
        self.flush_buffer()
        origin_pos = self.input_file.tell()
        self.input_file.seek(0)

        proc = subprocess.Popen(
            shell_cmd,
            shell=True,
            stdin=self.input_file.fileno(),
            stdout=subprocess.PIPE,
            universal_newlines=replace_EOL,
            preexec_fn=os.setsid if os.name == "posix" else None,
        )

        try:
            output, _ = proc.communicate(timeout=time_limit)
        except subprocess.TimeoutExpired:
            # proc.kill()  # didn't work because `shell=True`.
            self._kill_process_and_children(proc)
            raise
        else:
            if replace_EOL:
                self.output_file.write(output)
            else:
                os.write(self.output_file.fileno(), output)
        finally:
            self.input_file.seek(origin_pos)

        log.debug(self.output_filename, " done")

    def output_write(self, *args, **kwargs):
        """
        Write every element in *args into the output file. Splits with `separator`.
        It will convert every element into str.
        Args:
            *args: the elements to write
            separator: a string used to separate every element. Defaults to " ".
        """
        if self.output_file is None:
            raise ValueError("Output file is disabled")
        self.__write(self.output_file, *args, **kwargs)

    def output_writeln(self, *args, **kwargs):
        """
        Write every element in *args into the output file and turn to a new line.
        Splits with `separator`.
        It will convert every element into str.
        Args:
            *args: the elements to write
            separator: a string used to separate every element. Defaults to " ".
        """
        args = list(args)
        args.append("\n")
        self.output_write(*args, **kwargs)

    def output_clear_content(self, pos: int = 0):
        """
        Clear the content of output
        Args:
            pos: Where file will truncate
        """
        if self.output_file is None:
            raise ValueError("Output file is disabled")
        self.__clear(self.output_file, pos)

    def flush_buffer(self):
        """Flush the input file"""
        self.input_file.flush()
