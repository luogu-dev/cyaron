from ..utils import *
from .graderregistry import CYaRonGraders


@CYaRonGraders.grader("NOIPStyle")
def noipstyle(content, std):
    content_lines = strtolines(content.replace('\r\n', '\n'))
    std_lines = strtolines(std.replace('\r\n', '\n'))
    if len(content_lines) != len(std_lines):
        return False, 'Too many or too few lines.'

    for i in range(len(content_lines)):
        if std_lines[i] != content_lines[i]:
            for j in range(min(len(std_lines[i]), len(content_lines[i]))):
                if std_lines[i][j] != content_lines[i][j]:
                    return (False, 'On line %d column %d, read %s, expected %s.'
                            % (i + 1, j + 1, content_lines[i][j:j + 5], std_lines[i][j:j + 5]))
            if len(std_lines[i]) > len(content_lines[i]):
                return False, 'Too short on line %d.' % i
            if len(std_lines[i]) < len(content_lines[i]):
                return False, 'Too long on line %d.' % i

    return True, None