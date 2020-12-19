import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
encoding = 'utf-8'

def encode(data):
    idasstr = str(data)
    return b64e(zlib.compress(idasstr.encode(encoding), 9)).decode(encoding)

def decode(obscured):
    return zlib.decompress(b64d(obscured)).decode(encoding)


