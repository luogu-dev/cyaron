class Mismatch(ValueError):
    """exception for content mismatch"""
    def __init__(self, content, std, *args):
        """
        content -> content got
        std -> content expected
        """
        super(Mismatch, self).__init__(content, std, *args)
        self.content = content
        self.std = std

class HashMismatch(Mismatch):
    """exception for hash mismatch"""
    def __str__(self):
        return "Hash mismatch: read %s, expected %s" % (self.content, self.std)

class TextMismatch(Mismatch):
    """exception for text mismatch"""
    def __init__(self, content, std, err_msg, lineno=None, colno=None, content_token=None, std_token=None):
        super(TextMismatch, self).__init__(content, std, err_msg, lineno, colno, content_token, std_token)
        self.err_msg = err_msg.format(lineno, colno, content_token, std_token)
        self.lineno = lineno
        self.colno = colno
        self.content_token = content_token
        self.std_token = std_token

    def __str__(self):
        return self.err_msg
