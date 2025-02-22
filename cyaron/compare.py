from __future__ import absolute_import, print_function

import multiprocessing
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from io import open
from typing import List, Optional, Tuple, Union, cast

from cyaron.consts import *
from cyaron.graders import CYaRonGraders, GraderType3
from cyaron.utils import *

from . import log
from .io import IO


class CompareMismatch(ValueError):

    def __init__(self, name, mismatch):
        super(CompareMismatch, self).__init__(name, mismatch)
        self.name = name
        self.mismatch = mismatch

    def __str__(self):
        return "In program: '{}'. {}".format(self.name, self.mismatch)


PrgoramType = Union[str, Tuple[str, ...], List[str]]


class Compare:

    @staticmethod
    def __compare_two(name: PrgoramType, content: str, std: str,
                      input_content: str, grader: Union[str, GraderType3]):
        result, info = CYaRonGraders.invoke(grader, content, std,
                                            input_content)
        status = "Correct" if result else "!!!INCORRECT!!!"
        info = info if info is not None else ""
        log.debug("{}: {} {}".format(name, status, info))
        if not result:
            raise CompareMismatch(name, info)

    @staticmethod
    def __process_output_file(file: Union[str, IO]):
        if isinstance(file, IO):
            if file.output_filename is None:
                raise ValueError("IO object has no output file.")
            file.flush_buffer()
            with open(file.output_filename,
                      "r",
                      newline="\n",
                      encoding='utf-8') as f:
                return file.output_filename, f.read()
        else:
            with open(file, "r", newline="\n", encoding="utf-8") as f:
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
        kwargs = unpack_kwargs(
            "output",
            kwargs,
            (
                "std",
                ("grader", DEFAULT_GRADER),
                ("max_workers", -1),
                ("job_pool", None),
                ("stop_on_incorrect", None),
            ),
        )
        std: IO = kwargs["std"]
        grader = kwargs["grader"]
        max_workers = kwargs["max_workers"]
        job_pool = kwargs["job_pool"]
        if kwargs["stop_on_incorrect"] is not None:
            log.warn(
                "parameter stop_on_incorrect is deprecated and has no effect.")

        if (max_workers is None or max_workers >= 0) and job_pool is None:
            max_workers = cls.__normal_max_workers(max_workers)
            try:
                with ThreadPoolExecutor(max_workers=max_workers) as job_pool:
                    return cls.output(*files,
                                      std=std,
                                      grader=grader,
                                      max_workers=max_workers,
                                      job_pool=job_pool)
            except ImportError:
                pass

        def get_std():
            return cls.__process_output_file(std)[1]

        if job_pool is not None:
            std_answer = job_pool.submit(get_std).result()
        else:
            std_answer = get_std()

        with open(std.input_filename, "r", newline="\n",
                  encoding="utf-8") as input_file:
            input_text = input_file.read()

        def do(file):
            (file_name, content) = cls.__process_output_file(file)
            cls.__compare_two(file_name, content, std_answer, input_text,
                              grader)

        if job_pool is not None:
            job_pool.map(do, files)
        else:
            [x for x in map(do, files)]

    @classmethod
    def program(cls,
                *programs: Union[PrgoramType, Tuple[PrgoramType, float]],
                input: Union[IO, str],
                std: Optional[Union[str, IO]] = None,
                std_program: Optional[Union[str, Tuple[str, ...],
                                            List[str]]] = None,
                grader: Union[str, GraderType3] = DEFAULT_GRADER,
                max_workers: Optional[int] = -1,
                job_pool: Optional[ThreadPoolExecutor] = None,
                stop_on_incorrect=None):
        """
        Compare the output of the programs with the standard output.
        
        Args:
            programs: The programs to be compared.
            input: The input file.
            std: The standard output file.
            std_program: The program that generates the standard output.
            grader: The grader to be used.
            max_workers: The maximum number of workers.
            job_pool: The job pool.
            stop_on_incorrect: Deprecated and has no effect.
        """
        if stop_on_incorrect is not None:
            log.warn(
                "parameter stop_on_incorrect is deprecated and has no effect.")

        if (max_workers is None or max_workers >= 0) and job_pool is None:
            max_workers = cls.__normal_max_workers(max_workers)
            try:
                with ThreadPoolExecutor(max_workers=max_workers) as job_pool:
                    return cls.program(*programs,
                                       input=input,
                                       std=std,
                                       std_program=std_program,
                                       grader=grader,
                                       max_workers=max_workers,
                                       job_pool=job_pool)
            except ImportError:
                pass

        if isinstance(input, IO):
            input.flush_buffer()

        if std_program is not None:

            def get_std_from_std_program():
                with open(input.input_filename
                          if isinstance(input, IO) else input,
                          "r",
                          newline="\n",
                          encoding="utf-8") as input_file:
                    content = subprocess.check_output(
                        std_program,
                        shell=(not list_like(std_program)),
                        stdin=input_file,
                        universal_newlines=True,
                        encoding="utf-8")
                return content

            if job_pool is not None:
                std = job_pool.submit(get_std_from_std_program).result()
            else:
                std = get_std_from_std_program()
        elif std is not None:

            def get_std_from_std_file():
                return cls.__process_output_file(cast(Union[str, IO], std))[1]

            if job_pool is not None:
                std = job_pool.submit(get_std_from_std_file).result()
            else:
                std = get_std_from_std_file()
        else:
            raise TypeError(
                "program() missing 1 required non-None keyword-only argument: 'std' or 'std_program'"
            )

        with open(input.input_filename if isinstance(input, IO) else input,
                  "r",
                  newline="\n",
                  encoding="utf-8") as input_file:
            input_text = input_file.read()

        def do(program_name: Union[PrgoramType, Tuple[PrgoramType, float]]):
            timeout = None
            if isinstance(program_name, tuple) and len(program_name) == 2 and (
                    isinstance(program_name[1], float)
                    or isinstance(program_name[1], int)):
                program_name, timeout = cast(Tuple[PrgoramType, float],
                                             program_name)
            else:
                program_name = cast(PrgoramType, program_name)
            content = subprocess.check_output(
                list(program_name)
                if isinstance(program_name, tuple) else program_name,
                shell=(not list_like(program_name)),
                input=input_text,
                universal_newlines=True,
                encoding="utf-8",
                timeout=timeout)
            cls.__compare_two(program_name, content, std, input_text, grader)

        if job_pool is not None:
            job_pool.map(do, programs)
        else:
            for program in programs:
                do(program)
