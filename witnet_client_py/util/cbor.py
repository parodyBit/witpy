import cbor

'''
radon_to_cbor converts a RADON script to a cbor array
example:
    script = parse_map_json().get_map().get_float('value')
    radon_to_cbor([[0x77, [0x66, 0], [0x64, 'value']])
    > [131, 24, 119, 130, 24, 102, 0, 130, 24, 100, 101, 118, 97, 108, 117, 101]
'''
def radon_to_cbor(script):
    return list(cbor.dumps(script))

'''
cbor_to_radon converts a cbor array to a RADON script
example:
    cbor_to_radon([131, 24, 119, 130, 24, 102, 0, 130, 24, 100, 101, 118, 97, 108, 117, 101])
    > [[0x77, [0x66, 0], [0x64, 'value']]
'''
def cbor_to_radon(script):
    return cbor.loads(bytearray(script))
