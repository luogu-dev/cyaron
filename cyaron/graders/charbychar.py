from ..utils import *
from .graderregistry import CYaRonGraders
from .mismatch import TextMismatch


@CYaRonGraders.grader("CharByChar")
def charbychar(content, std):
    if len(content) != len(std):
        return False, TextMismatch(content, std, 'Too many or too few chars.')

    for i in range(len(content)):
        if std[i] != content[i]:
            return False, TextMismatch(conetnt, std, 'Character {} differ.',i)

    return True, None
