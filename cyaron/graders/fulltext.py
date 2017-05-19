import hashlib
from .graderregistry import CYaRonGraders

@CYaRonGraders.grader("FullText")
def fulltext(content, std):
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    std_hash = hashlib.sha256(std.encode('utf-8')).hexdigest()
    return (True, None) if content_hash == std_hash else (False, "Hash mismatch: read %s, expected %s" % (content_hash, std_hash))

