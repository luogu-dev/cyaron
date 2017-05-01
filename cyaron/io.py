from .utils import *
import subprocess


class IO(object):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            if not "file_prefix" in kwargs:
                raise Exception("You must specify either two file names or file_prefix.")

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
            self.input_filename = args[0]
            self.output_filename = None
        elif len(args) == 2:
            self.input_filename = args[0]
            self.output_filename = args[1]
        else:
            raise Exception("Invalid argument count")

        self.input_file = open(self.input_filename, 'w')
        self.output_file = open(self.output_filename, 'w') if self.output_filename else None

    def __del__(self):
        try:
            self.input_file.close()
            self.output_file.close()
        except Exception:
            pass

    @staticmethod
    def __write(file, *args, **kwargs):
        separator = kwargs.get("separator", " ")
        for arg in args:
            if list_like(arg):
                IO.__write(file, *arg, **kwargs)
            else:
                file.write(str(arg))
                if arg != "\n":
                    file.write(separator)

    def input_write(self, *args, **kwargs):
        IO.__write(self.input_file, *args, **kwargs)

    def input_writeln(self, *args, **kwargs):
        args = list(args)
        args.append("\n")
        self.input_write(*args, **kwargs)

    def output_gen(self, shell_cmd):
        self.input_file.close()
        with open(self.input_filename, 'r') as f:
            self.output_file.write(subprocess.check_output(shell_cmd, shell=True, stdin=f))

        self.input_file = open(self.input_filename, 'a')

    def output_write(self, *args, **kwargs):
        IO.__write(self.output_file, *args, **kwargs)

    def output_writeln(self, *args, **kwargs):
        args = list(args)
        args.append("\n")
        self.output_write(*args, **kwargs)
