def ati(array):
    """ati(array) -> list
        Convert all the elements in the array and return them in a list.
    """
    return [int(i) for i in array]


def list_like(data):
    """list_like(data) -> bool
        Judge whether the object data is like a list or a tuple.
        object data -> the data to judge
    """
    return isinstance(data, tuple) or isinstance(data, list)


def strtolines(str):
    lines = str.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()

    while len(lines) > 0 and len(lines[len(lines) - 1]) == 0:
        del lines[len(lines) - 1]
    return lines


def make_unicode(data):
    try:
        return unicode(data)
    except NameError:
        return str(data)