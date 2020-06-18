import cbor


def radon_to_cbor(script):
    """
    Converts a RADON script to a CBOR array

    >>> print(radon_to_cbor([[0x77, [0x66, 0], [0x64, 'value']]))
    >>> [131, 24, 119, 130, 24, 102, 0, 130, 24, 100, 101, 118, 97, 108, 117, 101]

    :param script: A list of RADON operations
    :return: A list of bytes in the CBOR format
    """
    return list(cbor.dumps(script))


def cbor_to_radon(script):
    """
    Converts a CBOR array to a RADON script

    >>> print(cbor_to_radon([131, 24, 119, 130, 24, 102, 0, 130, 24, 100, 101, 118, 97, 108, 117, 101]))
    >>> [[0x77, [0x66, 0], [0x64, 'value']]

    :param script: A list of bytes in CBOR format. This is how it is stored on the blockchain
    :return: A list of RADON operations
    """
    return cbor.loads(bytearray(script))
