import unittest
from cyaron import String


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