import importlib
import unittest
import sys
from cyaron import String
import re


class TestString(unittest.TestCase):

    def test_random_word(self):
        test = String.random(100, charset="abc")
        self.assertTrue(all(a in "abc" for a in test))

    def test_random_word_from_dict(self):
        my_dict = ["lorem", "ipsum", "dolor", "sit", "amet"]
        test = String.random(None, charset=my_dict)
        self.assertTrue(test in my_dict)

    def test_random_sentence(self):
        sentence = String.random_sentence(10, sentence_terminators=".")
        self.assertTrue(sentence[0].isupper())
        self.assertTrue(sentence[-1] == ".")
        self.assertTrue(sentence.count(" ") == 9)

    def test_random_paragraph(self):
        # Only test for Errors
        String.random_paragraph(10)

    def test_random_regular(self):
        pattern = r'[0-9]+\w_.{0,9}'
        sentence = String.random_regular(pattern, limit=5)
        self.assertTrue(re.match(pattern, sentence).group() == sentence)

    def test_import_without_sre_parse(self):
        # Python 3.15 removed the sre_parse module that xeger <= 0.4.0 imports.
        names = ["sre_parse", "xeger", "xeger.xeger", "cyaron.string"]
        saved = {
            name: sys.modules.pop(name)
            for name in names if name in sys.modules
        }
        cyaron = sys.modules["cyaron"]
        saved_attr = cyaron.string
        sys.modules["sre_parse"] = None  # makes "import sre_parse" fail
        try:
            string_module = importlib.import_module("cyaron.string")
            pattern = r'[0-9]+\w_.{0,9}'
            sentence = string_module.String.random_regular(pattern, limit=5)
            self.assertTrue(re.match(pattern, sentence).group() == sentence)
        finally:
            for name in names:
                sys.modules.pop(name, None)
            sys.modules.update(saved)
            cyaron.string = saved_attr
