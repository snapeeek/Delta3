from Delta3Mini import key

encoding = 'utf-8'


def encode(id):
    idasstr = str(id)
    encoded = key.encrypt(idasstr.encode(encoding))
    return encoded.decode(encoding)


def decode(id):
    encoded= bytes(id,encoding=encoding)
    return key.decrypt(encoded).decode(encoding)
