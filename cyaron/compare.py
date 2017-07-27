from __future__ import absolute_import, print_function
from cyaron import IO, log
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
        (log.print if result else log.error)("%s: %s %s" % (name, status, info))

        stop_on_incorrect = kwargs.get("stop_on_incorrect", False)
        raise_on_incorrect = kwargs.get("raise_on_incorrect", False)
        dump_on_incorrect = kwargs.get("dump_on_incorrect", True)
        custom_dump_data = kwargs.get("dump_data", None)
        if (stop_on_incorrect or raise_on_incorrect) and not result:
            if custom_dump_data:
                (dump_name, dump_lambda) = custom_dump_data
                with open(dump_name, "w", newline='\n') as f:
                    f.write(dump_lambda())

            if dump_on_incorrect:
                with open("std.out", "w", newline='\n') as f:
                    f.write(std)
                with open("%s.out" % name, "w", newline='\n') as f:
                    f.write(content)

            log.info("Relevant files dumped.")

            if stop_on_incorrect:
                sys.exit(1)
            else:
                raise info


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
            raise TypeError("You must specify some files to compare.")

        if "std" not in kwargs:
            raise TypeError("You must specify a std.")
        (_, std) = Compare.__process_file(kwargs["std"])

        grader = kwargs.get("grader", DEFAULT_GRADER)
        del kwargs["std"]
        try: del kwargs["grader"]
        except KeyError: pass

        for file in args:
            (file_name, content) = Compare.__process_file(file)
            Compare.__compare_two(file_name, content, std, grader, **kwargs)

    @staticmethod
    def program(*args, **kwargs):
        if len(args) == 0:
            raise TypeError("You must specify some programs to compare.")

        if "input" not in kwargs:
            raise TypeError("You must specify an input.")
        input = kwargs['input']
        del kwargs['input']
        if not isinstance(input, IO):
            raise TypeError("Input must be an IO instance.")
        input.flush_buffer()
        input.input_file.seek(0)

        std = None
        if "std" not in kwargs and "std_program" not in kwargs:
            raise TypeError("You must specify a std or a std_program.")
        else:
            if "std_program" in kwargs:
                std = make_unicode(subprocess.check_output(kwargs['std_program'], shell=True, stdin=input.input_file, universal_newlines=True))
                del kwargs['std_program']
            else:
                (_, std) = Compare.__process_file(kwargs["std"])
                del kwargs['std']

        grader = kwargs.get("grader", DEFAULT_GRADER)
        try: del kwargs["grader"]
        except KeyError: pass

        for program_name in args:
            kws = kwargs.copy()
            input.input_file.seek(0)
            content = make_unicode(subprocess.check_output(program_name, shell=True, stdin=input.input_file, universal_newlines=True))

            input.input_file.seek(0)
            kws['dump_data'] = kws.get('dump_data', ("error_input.in", lambda: input.input_file.read())) # Lazy dump
            Compare.__compare_two(program_name, content, std, grader,
                                  **kws)

        input.input_file.seek(0, 2)
