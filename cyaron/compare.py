from cyaron import IO
from cyaron.consts import *
from cyaron.graders import CYaRonGraders
import subprocess


class Compare:
    @staticmethod
    def __compare_two(name, content, std, grader):
        (result, info) = CYaRonGraders.invoke(grader, content, std)

        info = info if info is not None else ""
        status = "Correct" if result else "!!!INCORRECT!!!"
        print("%s: %s %s" % (name, status, info))

    @staticmethod
    def __process_file(file):
        if isinstance(file, IO):
            file.flush_buffer()
            file.output_file.seek(0)
            return file.output_filename, file.output_file.read()
        else:
            with open(file, "r") as f:
                return file, f.read()

    @staticmethod
    def output(*args, **kwargs):
        if len(args) == 0:
            raise Exception("You must specify some files to compare.")

        if "std" not in kwargs:
            raise Exception("You must specify a std.")
        (_, std) = Compare.__process_file(kwargs["std"])

        grader = kwargs.get("grader", DEFAULT_GRADER)

        for file in args:
            (file_name, content) = Compare.__process_file(file)
            Compare.__compare_two(file_name, content, std, grader)

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
                std = subprocess.check_output(kwargs['std_program'], shell=True, stdin=input.input_file).decode('ascii')
            else:
                (_, std) = Compare.__process_file(kwargs["std"])

        grader = kwargs.get("grader", DEFAULT_GRADER)

        for program_name in args:
            content = subprocess.check_output(program_name, shell=True, stdin=input.input_file)
            Compare.__compare_two(program_name, content, std, grader)


