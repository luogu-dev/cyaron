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
    def __init__(self, content, std, content_hash, std_hash):
        """
        content -> content got
        std -> content expected
        content_hash -> hash of content
        std_hash -> hash of std
        """
        super(HashMismatch, self).__init__(content, std, content_hash, std_hash)
        self.content_hash = content_hash
        self.std_hash = std_hash

    def __str__(self):
        return "Hash mismatch: read %s, expected %s" % (self.content_hash, self.std_hash)

class TextMismatch(Mismatch):
    """exception for text mismatch"""
    def __init__(self, content, std, err_msg, lineno=None, colno=None, content_token=None, std_token=None):
        """
        content -> content got
        std -> content expected
        err_msg -> error message template like "wrong on line {} col {} read {} expected {}"
        lineno -> line number
        colno -> column number
        content_token -> the token of content mismatch
        std_token -> the token of std
        """
        super(TextMismatch, self).__init__(content, std, err_msg, lineno, colno, content_token, std_token)
        self.err_msg = err_msg.format(lineno, colno, content_token, std_token)
        self.lineno = lineno
        self.colno = colno
        self.content_token = content_token
        self.std_token = std_token

    def __str__(self):
        return self.err_msg
