from reedsolo import RSCodec

def ecc_add(data: bytes, strength=10):
    rsc = RSCodec(strength)
    return rsc.encode(data)

def ecc_remove(data: bytes, strength=10):
    rsc = RSCodec(strength)
    return rsc.decode(data)
