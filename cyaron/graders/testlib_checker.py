import tempfile
import subprocess
import os
import xml.etree.ElementTree as xmlElementTree
from typing import Optional

STDOUT_DEV = "con" if os.name == "nt" else "/dev/stdout"

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
        with tempfile.NamedTemporaryFile(
                'w') as inf, tempfile.NamedTemporaryFile(
                    'w') as outf, tempfile.NamedTemporaryFile('w') as ansf:
            inf.write(ins)
            outf.write(outs)
            ansf.write(ans)
            inf.flush()
            outf.flush()
            ansf.flush()
            result = subprocess.run((self.checker_path, inf.name, outf.name,
                                     ansf.name, STDOUT_DEV, '-appes'),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    check=False)
            if result.stderr.strip() != 'See file to check exit message':
                raise ValueError("Invalid output from checker: " +
                                 result.stderr)
            checker_output = result.stdout

            result_element = xmlElementTree.fromstring(checker_output)
            if result_element.tag != 'result':
                raise ValueError("Invalid output from checker")
            result_text = result_element.text
            result_outcome = result_element.get('outcome')
            if result_outcome is None:
                raise ValueError("Invalid output from checker")
            result_pctype = result_element.get('pctype')
            return result_outcome == 'accepted', TestlibCheckerResult(
                result_text, result_outcome, result_pctype)
