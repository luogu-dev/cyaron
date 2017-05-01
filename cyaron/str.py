from .consts import ALPHABET_SMALL, SENTENCE_SEPARATORS, SENTENCE_TERMINATORS
from .utils import *
from functools import reduce
import random


class String:
    @staticmethod
    def random(length_range, **kwargs):
        length = length_range
        if list_like(length_range):
            length = random.randint(length_range[0], length_range[1])
        charset = kwargs.get("charset", ALPHABET_SMALL)

        if list_like(charset):
            return random.choice(charset)
        else:
            return "".join(random.choice(charset) for i in range(length))

    @staticmethod
    def random_sentence(word_count_range, **kwargs):
        word_count = word_count_range
        if list_like(word_count_range):
            word_count = random.randint(word_count_range[0], word_count_range[1])

        word_length_range = kwargs.get("word_length_range", (3, 8))
        first_letter_uppercase = kwargs.get("first_letter_uppercase", True)
        charset = kwargs.get("charset", ALPHABET_SMALL)

        word_separators = kwargs.get("word_separators", " ")
        if word_separators is None or len(word_separators) == 0:
            word_separators = [""]

        sentence_terminators = kwargs.get("sentence_terminators", SENTENCE_TERMINATORS)
        if sentence_terminators is None or len(sentence_terminators) == 0:
            sentence_terminators = [""]

        words = []
        for i in range(word_count):
            words.append(String.random(word_length_range, charset=charset))
        if first_letter_uppercase:
            words[0] = words[0].capitalize()

        # We cannot just `sentence_separators.join()` here
        # since we want to randomly select one on each join
        sentence = reduce(lambda x, y: x + random.choice(word_separators) + y, words)
        sentence += random.choice(sentence_terminators)

        return sentence

    @staticmethod
    def random_paragraph(sentence_count_range, **kwargs):
        sentence_count = sentence_count_range
        if list_like(sentence_count_range):
            sentence_count = random.randint(sentence_count_range[0], sentence_count_range[1])

        first_letter_uppercase = kwargs.get("first_letter_uppercase", True)
        kwargs["first_letter_uppercase"] = False

        termination_percentage = kwargs.get("termination_percentage", 0.3)
        if not 0 <= termination_percentage <= 1:
            raise Exception("Invalid termination_percentage")

        sentence_joiners = kwargs.get("sentence_joiners", " ")
        if sentence_joiners is None or len(sentence_joiners) == 0:
            sentence_joiners = [""]

        sentence_separators = kwargs.get("sentence_separators", SENTENCE_SEPARATORS)
        if sentence_separators is None or len(sentence_separators) == 0:
            sentence_separators = [""]

        sentence_terminators = kwargs.get("sentence_terminators", SENTENCE_TERMINATORS)
        if sentence_terminators is None or len(sentence_terminators) == 0:
            sentence_terminators = [""]
        kwargs["sentence_terminators"] = None

        sentences = []
        capitalize_next_sentence = True
        for i in range(sentence_count):
            string = String.random_sentence(**kwargs)
            sep_or_term = random.random()

            if capitalize_next_sentence and first_letter_uppercase:
                string = string.capitalize()

            if sep_or_term < termination_percentage or i == sentence_count - 1:
                string += random.choice(sentence_terminators)
                capitalize_next_sentence = True
            else:
                string += random.choice(sentence_separators)
                capitalize_next_sentence = False

            sentences.append(string)

        paragraph = reduce(lambda x, y: x + random.choice(sentence_joiners) + y, sentences)
        return paragraph

