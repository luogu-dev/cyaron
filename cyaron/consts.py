import math
import string

"""Constants Package.
Constants:
ALPHABET_SMALL -> All the lower ascii letters
ALPHABET_CAPITAL -> All the upper ascii letters
ALPHABET -> All the upper ascii letters
NUMBERS -> All the numbers(0-9)
SENTENCE_SEPARATORS -> Includes 70% ",", 20% ";" and 10% ":"
SENTENCE_TERMINATORS -> Includes 80% "." and 20% "!"
"""
PI = math.pi
E = math.e

ALPHABET_SMALL = string.ascii_lowercase
ALPHABET_CAPITAL = string.ascii_uppercase
ALPHABET = string.ascii_uppercase
NUMBERS = string.digits
SENTENCE_SEPARATORS = ',,,,,,,;;:' # 70% ',' 20% ';' 10% ':'
SENTENCE_TERMINATORS = '....!' # 80% '.' 20% '!'
