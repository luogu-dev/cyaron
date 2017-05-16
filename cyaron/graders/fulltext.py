import hashlib
from .graderregistry import CYaRonGraders

@CYaRonGraders.grader("FullText")
def fulltext(content, std):
    content_hash = hashlib.sha256(content).hexdigest()
    std_hash = hashlib.sha256(std).hexdigest()
    return True, None if content_hash == std_hash else False, "Hash mismatch: read %s, expected %s" % (content_hash, std_hash)

