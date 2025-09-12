import subprocess
import unittest
import os
import tempfile
import shutil
import sys


class TestGeneral(unittest.TestCase):

    def setUp(self):
        self.original_directory = os.getcwd()
        self.temp_directory = tempfile.mkdtemp()
        os.chdir(self.temp_directory)

    def tearDown(self):
        os.chdir(self.original_directory)
        try:
            shutil.rmtree(self.temp_directory)
        except:
            pass

    def test_randseed_arg(self):
        with open("test_randseed.py", 'w', encoding='utf-8') as f:
            f.write("import cyaron as c\n"
                    "c.process_args()\n"
                    "for i in range(10):\n"
                    "    print(c.randint(1,1000000000),end=' ')\n")

        env = os.environ.copy()
        env['PYTHONPATH'] = self.original_directory + os.pathsep + env.get(
            'PYTHONPATH', '')
        result = subprocess.run([
            sys.executable, 'test_randseed.py',
            '--randseed=pinkrabbit147154220'
        ],
                                env=env,
                                stdout=subprocess.PIPE,
                                universal_newlines=True,
                                check=True)
        self.assertEqual(
            result.stdout,
            "243842479 490459912 810766286 646030451 191412261 929378523 273000814 982402032 436668773 957169453 "
        )
