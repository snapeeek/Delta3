from Delta3Mini import key

encoding = 'utf-8'


def encode(id):
    return key.encrypt(id.encode(encoding))


def decode(id):
    return key.decrypt(id).decode(encoding)
