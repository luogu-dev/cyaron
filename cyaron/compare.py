from __future__ import absolute_import, print_function
from cyaron import IO, log
from cyaron.utils import *
from cyaron.consts import *
from cyaron.graders import CYaRonGraders
import subprocess
import multiprocessing
import sys
from io import open
import os


class CompareMismatch(ValueError):
    def __init__(self, name, mismatch):
        super(CompareMismatch, self).__init__(name, mismatch)
        self.name = name
        self.mismatch = mismatch

    def __str__(self):
        return 'In program: \'{}\'. {}'.format(self.name,self.mismatch)


class Compare:
    @staticmethod
    def __compare_two(name, content, std, grader):
        (result, info) = CYaRonGraders.invoke(grader, content, std)
        status = "Correct" if result else "!!!INCORRECT!!!"
        info = info if info is not None else ""
        log.debug("{}: {} {}".format(name, status, info))
        if not result:
            raise CompareMismatch(name, info)

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
    def __normal_max_workers(workers):
        if workers is None:
            if sys.version_info < (3, 5):
                cpu = multiprocessing.cpu_count()
                return cpu * 5 if cpu is not None else 1
        return workers

    @classmethod
    def output(cls, *files, **kwargs):
        kwargs = unpack_kwargs('output', kwargs, ('std', ('grader', DEFAULT_GRADER), ('max_workers', -1),
                                                  ('job_pool', None), ('stop_on_incorrect', None)))
        std = kwargs['std']
        grader = kwargs['grader']
        max_workers = kwargs['max_workers']
        job_pool = kwargs['job_pool']
        if kwargs['stop_on_incorrect'] is not None:
            log.warn("parameter stop_on_incorrect is deprecated and has no effect.")

        if (max_workers is None or max_workers >= 0) and job_pool is None:
            max_workers = cls.__normal_max_workers(max_workers)
            try:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=max_workers) as job_pool:
                    return cls.output(*files, std=std, grader=grader, max_workers=max_workers, job_pool=job_pool)
            except ImportError:
                pass

        def get_std():
            return cls.__process_file(std)[1]
        if job_pool is not None:
            std = job_pool.submit(get_std).result()
        else:
            std = get_std()

        def do(file):
            (file_name, content) = cls.__process_file(file)
            cls.__compare_two(file_name, content, std, grader)

        if job_pool is not None:
            job_pool.map(do, files)
        else:
            [x for x in map(do, files)]

    @classmethod
    def program(cls, *programs, **kwargs):
        kwargs = unpack_kwargs('program', kwargs, ('input', ('std', None), ('std_program', None),
                                                   ('grader', DEFAULT_GRADER), ('max_workers', -1),
                                                   ('job_pool', None), ('stop_on_incorrect', None)))
        input = kwargs['input']
        std = kwargs['std']
        std_program = kwargs['std_program']
        grader = kwargs['grader']
        max_workers = kwargs['max_workers']
        job_pool = kwargs['job_pool']
        if kwargs['stop_on_incorrect'] is not None:
            log.warn("parameter stop_on_incorrect is deprecated and has no effect.")

        if (max_workers is None or max_workers >= 0) and job_pool is None:
            max_workers = cls.__normal_max_workers(max_workers)
            try:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=max_workers) as job_pool:
                    return cls.program(*programs, input=input, std=std, std_program=std_program, grader=grader, max_workers=max_workers, job_pool=job_pool)
            except ImportError:
                pass

        if not isinstance(input, IO):
            raise TypeError("expect {}, got {}".format(type(IO).__name__, type(input).__name__))
        input.flush_buffer()
        input.input_file.seek(0)

        if std_program is not None:
            def get_std():
                with open(os.dup(input.input_file.fileno()), 'r', newline='\n') as input_file:
                    content = make_unicode(subprocess.check_output(std_program, shell=(not list_like(std_program)), stdin=input.input_file, universal_newlines=True))
                    input_file.seek(0)
                return content
            if job_pool is not None:
                std = job_pool.submit(get_std).result()
            else:
                std = get_std()
        elif std is not None:
            def get_std():
                return cls.__process_file(std)[1]
            if job_pool is not None:
                std = job_pool.submit(get_std).result()
            else:
                std = get_std()
        else:
            raise TypeError('program() missing 1 required non-None keyword-only argument: \'std\' or \'std_program\'')

        def do(program_name):
            timeout = None
            if list_like(program_name) and len(program_name) == 2 and int_like(program_name[-1]):
                program_name, timeout = program_name
            with open(os.dup(input.input_file.fileno()), 'r', newline='\n') as input_file:
                if timeout is None:
                    content = make_unicode(subprocess.check_output(program_name, shell=(not list_like(program_name)), stdin=input_file, universal_newlines=True))
                else:
                    content = make_unicode(subprocess.check_output(program_name, shell=(not list_like(program_name)), stdin=input_file, universal_newlines=True, timeout=timeout))
                input_file.seek(0)
            cls.__compare_two(program_name, content, std, grader)

        if job_pool is not None:
            job_pool.map(do, programs)
        else:
            [x for x in map(do, programs)]
