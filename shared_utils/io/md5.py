import hashlib


def md5(value):
    return hashlib.md5(value.encode()).hexdigest()
