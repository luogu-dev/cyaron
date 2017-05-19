from __future__ import absolute_import
from cyaron import IO
from cyaron.utils import *
from cyaron.consts import *
from cyaron.graders import CYaRonGraders
import subprocess
import sys
from io import open


class Compare:
    @staticmethod
    def __compare_two(name, content, std, grader, **kwargs):
        (result, info) = CYaRonGraders.invoke(grader, content, std)

        info = info if info is not None else ""
        status = "Correct" if result else "!!!INCORRECT!!!"
        print("%s: %s %s" % (name, status, info))

        stop_on_incorrect = kwargs.get("stop_on_incorrect", False)
        custom_dump_data = kwargs.get("dump_data", None)
        if stop_on_incorrect and not result:
            if custom_dump_data:
                (dump_name, dump_lambda) = custom_dump_data
                with open(dump_name, "w", newline='\n') as f:
                    f.write(dump_lambda())

            with open("std.out", "w", newline='\n') as f:
                f.write(std)
            with open("%s.out" % name, "w", newline='\n') as f:
                f.write(content)

            print("Relevant files dumped.")

            sys.exit(0)


    @staticmethod
    def __process_file(file):
        if isinstance(file, IO):
            file.flush_buffer()
            file.output_file.seek(0)
            return file.output_filename, file.output_file.read()
        else:
            with open(file, "r", newline='\n') as f:
                return file, f.read()

    @staticmethod
    def output(*args, **kwargs):
        if len(args) == 0:
            raise Exception("You must specify some files to compare.")

        if "std" not in kwargs:
            raise Exception("You must specify a std.")
        (_, std) = Compare.__process_file(kwargs["std"])

        grader = kwargs.get("grader", DEFAULT_GRADER)
        stop_on_incorrect = kwargs.get("stop_on_incorrect", False)

        for file in args:
            (file_name, content) = Compare.__process_file(file)
            Compare.__compare_two(file_name, content, std, grader, stop_on_incorrect=stop_on_incorrect)

    @staticmethod
    def program(*args, **kwargs):
        if len(args) == 0:
            raise Exception("You must specify some programs to compare.")

        if "input" not in kwargs:
            raise Exception("You must specify an input.")
        input = kwargs['input']
        if not isinstance(input, IO):
            raise Exception("Input must be an IO instance.")
        input.flush_buffer()
        input.input_file.seek(0)

        std = None
        if "std" not in kwargs and "std_program" not in kwargs:
            raise Exception("You must specify a std or a std_program.")
        else:
            if "std_program" in kwargs:
                std = make_unicode(subprocess.check_output(kwargs['std_program'], shell=True, stdin=input.input_file, universal_newlines=True))
            else:
                (_, std) = Compare.__process_file(kwargs["std"])

        grader = kwargs.get("grader", DEFAULT_GRADER)
        stop_on_incorrect = kwargs.get("stop_on_incorrect", False)

        for program_name in args:
            input.input_file.seek(0)
            content = make_unicode(subprocess.check_output(program_name, shell=True, stdin=input.input_file, universal_newlines=True))

            input.input_file.seek(0)
            Compare.__compare_two(program_name, content, std, grader,
                                  stop_on_incorrect=stop_on_incorrect,
                                  dump_data=("error_input.in", lambda: input.input_file.read())) # Lazy dump

        input.input_file.seek(0, 2)
