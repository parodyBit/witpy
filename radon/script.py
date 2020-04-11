from .types import typeSystem
import re
import binascii
import cbor
from queue import Queue


class Script:

    def __init__(self, ):
        self.types = []
        self.script = []
        self.method = ''

    def encode(self):
        return radon_to_cbor(self.script)


def radon_to_cbor(script):
    return list(cbor.dumps(script))


def cbor_to_radon(script):
    return cbor.loads(bytearray(script))


def parse_op(op):
    operator = op.split('(')[0]
    var = re.findall('"([^"]*)"', op)
    return [operator, var]


def find_type(op):
    _type = None
    count = 0
    for t in typeSystem:
        if op[0] in typeSystem[t]:
            _type = t
            count += 1
    if count is 1:
        pass  # There can only be one
    else:
        _type = None
    return _type


def method_from_script(script):
    rad = cbor_to_radon(script)
    first_type = rad[0]
    method = ''
    next_type = None
    # first type
    for _type in typeSystem:
        for sub in typeSystem[_type]:
            if typeSystem[_type][sub][0] == first_type:
                first_type = _type
                next_type = typeSystem[_type][sub][1][0]
                method += f'{sub}().'
    rad.pop(0)
    for item in rad:
        op = ''
        for sub in typeSystem[next_type]:
            if typeSystem[next_type][sub][0] == item[0]:
                if isinstance(item[1], str):
                    method += f'{sub}("{item[1]}").'
                if isinstance(item[1], int):
                    method += f'{sub}().'
                op = sub
        if item != rad[len(rad)-1]:
            next_type = typeSystem[next_type][op][1][0]
    return method[:-1]


def script_from_str(string):
    raw = string.split('.')
    operations = Queue(maxsize=0)
    script = Script()

    first_type = find_type(parse_op(raw[0]))
    last_type = first_type
    script.types.append(first_type)

    for item in raw:
        operations.put(item)
        method = parse_op(item)[0]
        script.types.append(typeSystem[last_type][method][1])
        last_type = typeSystem[last_type][method][1][0]
    # reset the last last_type for the queue loop
    last_type = None
    next_type = None
    while not operations.empty():
        op = parse_op(operations.get())
        operator = op[0]

        # check if it is the first operator
        if next_type is None:
            for _type in typeSystem:

                try:
                    last_type = op[0]
                    next_type = typeSystem[_type][operator][1][0]
                    script.script.append(typeSystem[_type][operator][0])
                except KeyError:
                    pass
        try:
            val = 0 if len(op[1]) < 1 else op[1][0]
            script.script.append([typeSystem[last_type][op[0]][0], val])
            next_type = typeSystem[next_type][op[0]][1][0]
        except KeyError:
            pass

        if next_type is 'Inner':
            next_type = last_type
        elif next_type is 'Match':
            pass
        elif next_type is 'Same':
            pass

        last_type = next_type

    script.method = method_from_script(radon_to_cbor(script.script))
    return script
