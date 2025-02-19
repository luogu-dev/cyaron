import tempfile
import subprocess
import xml.etree.ElementTree as xmlElementTree
from typing import Optional
from os.path import join as path_join

__all__ = ["TestlibChecker"]


class TestlibCheckerResult:

    def __init__(self, result: Optional[str], outcome: str,
                 pctype: Optional[str]):
        self.result = result
        self.outcome = outcome
        self.pctype = pctype

    def __str__(self):
        return ' '.join([self.outcome] +
                        ([] if self.pctype is None else [f'({self.pctype})']) +
                        ([] if self.result is None else [self.result]))


class TestlibChecker:
    """
    A grader that uses the testlib checker.
    """

    def __init__(self, checker_path: str):
        self.checker_path = checker_path

    def __call__(self, outs: str, ans: str, ins: str):
        with tempfile.TemporaryDirectory() as checker_temp_dir, \
             open(path_join(checker_temp_dir, 'input.txt'), 'w', newline='\n') as inf, \
             open(path_join(checker_temp_dir, 'output.txt'), 'w', newline='\n') as outf, \
             open(path_join(checker_temp_dir, 'answer.txt'), 'w', newline='\n') as ansf:
            inf.write(ins)
            outf.write(outs)
            ansf.write(ans)
            inf.flush()
            outf.flush()
            ansf.flush()
            checker_output_file = path_join(checker_temp_dir,
                                            'checker_output.xml')

            result = subprocess.run((self.checker_path, inf.name, outf.name,
                                     ansf.name, checker_output_file, '-appes'),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    check=False)
            if result.stderr.strip() != 'See file to check exit message':
                raise ValueError("Invalid output from checker: " +
                                 result.stderr)

            result_element = xmlElementTree.parse(
                checker_output_file).getroot()
            if result_element.tag != 'result':
                raise ValueError("Invalid output from checker")
            result_text = result_element.text
            result_outcome = result_element.get('outcome')
            if result_outcome is None:
                raise ValueError("Invalid output from checker")
            result_pctype = result_element.get('pctype')
            return result_outcome == 'accepted', TestlibCheckerResult(
                result_text, result_outcome, result_pctype)
