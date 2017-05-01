def ati(array):
    return [int(i) for i in array]

def list_like(data):
    return isinstance(data, tuple) or isinstance(data, list)