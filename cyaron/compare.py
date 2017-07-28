from __future__ import absolute_import, print_function
from cyaron import IO, log
from cyaron.utils import *
from cyaron.consts import *
from cyaron.graders import CYaRonGraders
import subprocess
import sys
from io import open
import os


class Compare:
    @staticmethod
    def __compare_two(name, content, std, grader):
        (result, info) = CYaRonGraders.invoke(grader, content, std)
        status = "Correct" if result else "!!!INCORRECT!!!"
        info = info if info is not None else ""
        log.debug("{}: {} {}".format(name, status, info))
        if not result:
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
    def output(*files, std, grader=DEFAULT_GRADER, max_workers=-1, job_pool=None):
        if (max_workers is None or max_workers >= 0) and job_pool is None:
            try:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=max_workers) as job_pool:
                    return Compare.output(*files, std=std, grader=grader, max_workers=max_workers, job_pool=job_pool)
            except ImportError:
                pass

        def get_std():
            nonlocal std
            (_, std) = Compare.__process_file(std)
        if job_pool is not None:
            job_pool.submit(get_std).result()
        else:
            get_std()

        def do(file):
            (file_name, content) = Compare.__process_file(file)
            Compare.__compare_two(file_name, content, std, grader)

        if job_pool is not None:
            job_pool.map(do, files)
        else:
            [x for x in map(do, files)]

    @staticmethod
    def program(*programs, input, std=None, std_program=None, grader=DEFAULT_GRADER, max_workers=-1, job_pool=None):
        if (max_workers is None or max_workers >= 0) and job_pool is None:
            try:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=max_workers) as job_pool:
                    return Compare.program(*programs, input=input, std=std, std_program=std_program, grader=grader, max_workers=max_workers, job_pool=job_pool)
            except ImportError:
                pass

        if not isinstance(input, IO):
            raise TypeError("expect {}, got {}".format(type(IO).__name__, type(input).__name__))
        input.flush_buffer()
        input.input_file.seek(0)

        if std_program is not None:
            def get_std():
                nonlocal std
                std = make_unicode(subprocess.check_output(std_program, shell=(not list_like(std_program)), stdin=input.input_file, universal_newlines=True))
            if job_pool is not None:
                job_pool.submit(get_std).result()
            else:
                get_std()
        elif std is not None:
            def get_std():
                nonlocal std
                (_, std) = Compare.__process_file(std)
            if job_pool is not None:
                job_pool.submit(get_std).result()
            else:
                get_std()
        else:
            raise TypeError('program() missing 1 required non-None positional argument: \'std\' or \'std_program\'')

        def do(program_name):
            with os.fdopen(os.dup(input.input_file.fileno()), 'r', newline='\n') as input_file:
                content = make_unicode(subprocess.check_output(program_name, shell=(not list_like(program_name)), stdin=input_file, universal_newlines=True))
            Compare.__compare_two(program_name, content, std, grader)

        if job_pool is not None:
            job_pool.map(do, programs)
        else:
            [x for x in map(do, programs)]
