from ..utils import *
from .graderregistry import CYaRonGraders
from .mismatch import TextMismatch


@CYaRonGraders.grader("NOIPStyle")
def noipstyle(content, std):
    content_lines = strtolines(content.replace('\r\n', '\n'))
    std_lines = strtolines(std.replace('\r\n', '\n'))
    if len(content_lines) != len(std_lines):
        return False, TextMismatch(content, std, 'Too many or too few lines.')

    for i in range(len(content_lines)):
        if std_lines[i] != content_lines[i]:
            for j in range(min(len(std_lines[i]), len(content_lines[i]))):
                if std_lines[i][j] != content_lines[i][j]:
                    return (False,
                            TextMismatch(
                                content, std,
                                'On line {} column {}, read {}, expected {}.',
                                i + 1, j + 1, content_lines[i][j:j + 5],
                                std_lines[i][j:j + 5]))
            if len(std_lines[i]) > len(content_lines[i]):
                return False, TextMismatch(
                    content, std, 'Too short on line {}.', i + 1, j + 1,
                    content_lines[i][j:j + 5], std_lines[i][j:j + 5])
            if len(std_lines[i]) < len(content_lines[i]):
                return False, TextMismatch(
                    content, std, 'Too long on line {}.', i + 1, j + 1,
                    content_lines[i][j:j + 5], std_lines[i][j:j + 5])

    return True, None
