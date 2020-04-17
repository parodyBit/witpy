from .types import *
from witnet_client_py.util import radon_to_cbor, cbor_to_radon, valid_url, parse_op
from queue import Queue


def find_type(op):
    _type = None
    count = 0
    for t in type_system:
        if op[0] in type_system[t]:
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
    for _type in type_system:
        for sub in type_system[_type]:
            if type_system[_type][sub][0] == first_type:
                first_type = _type
                next_type = type_system[_type][sub][1][0]
                method += f'{sub}().'
    rad.pop(0)
    for item in rad:
        op = ''
        for sub in type_system[next_type]:
            if type_system[next_type][sub][0] == item[0]:
                if isinstance(item[1], str):
                    method += f'{sub}("{item[1]}").'
                if isinstance(item[1], int):
                    method += f'{sub}().'
                op = sub
        if item != rad[len(rad) - 1]:
            next_type = type_system[next_type][op][1][0]
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
        script.types.append(type_system[last_type][method][1])
        last_type = type_system[last_type][method][1][0]
    # reset the last last_type for the queue loop
    last_type = None
    next_type = None
    while not operations.empty():
        op = parse_op(operations.get())
        operator = op[0]

        # check if it is the first operator
        if next_type is None:
            for _type in type_system:

                try:
                    last_type = op[0]
                    next_type = type_system[_type][operator][1][0]
                    script.script.append(type_system[_type][operator][0])
                except KeyError:
                    pass
        try:
            if type(op[1]) is int:
                val = op[1]
            else:
                val = 0 if len(op[1]) < 1 else op[1][0]
            script.script.append([type_system[last_type][op[0]][0], val])
            next_type = type_system[next_type][op[0]][1][0]
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


class Script:
    def __init__(self):
        self.types = []
        self.ops = []
        self.args = []
        self.script = []


class Aggregator(Script):
    def __init__(self, filters=None, reducer=None):
        super().__init__()
        self.filters = [{'args': filters[0][1], 'op': filters[0][0]}]
        self.reducer = reducer


class Tally(Script):
    def __init__(self, filters=None, reducer=None):
        super().__init__()
        self.filters = [{'args': filters[0][1], 'op': filters[0][0]}]
        self.reducer = reducer


class Source(Script):

    def __init__(self, url):
        super().__init__()
        self.rad = []
        self.url = ''
        self.prev_type = None
        self.first_type = None
        self.next_type = None
        if type(url) != str:
            print(f'Error: Invalid Type. expected str - received {type(url)}.')

        if valid_url(url):
            self.url = url
            self.args.append(url)
            self.prev_type = TYPES.STRING
            self.first_type = TYPES.STRING
            self.types.append(self.prev_type)
        else:
            print('Error: Invalid URL')

    def encode(self):
        script = []
        print(self.types)
        print(self.ops)
        print(self.args)
        idx = 0
        for op in self.ops:
            _type, arg = self.types[idx], self.args[idx]

            # print(_type, op, arg, idx)
            # first item?
            if idx == 0:
                script.append(type_system[_type][op][0])
            # last item?
            elif idx == len(self.args) - 1:
                print('[arg] ', arg)
                if arg is None:
                    script.append(type_system[_type][op][0])
                else:
                    script.append([type_system[_type][op][0], arg])
            else:
                script.append([type_system[_type][op][0], arg])
            idx += 1

        self.script = script
        return self

    def _is_valid_operation(self, op):
        # is the operation valid for the previous type
        if op in type_system[self.prev_type]:
            return True
        return False

    def _operation(self, **kargs):
        if self._is_valid_operation(kargs['op']):
            if len(kargs['arg']) > 0:
                self.args.append(kargs['arg'][0])
            else:
                self.args.append(None)
            self.prev_type = kargs['next_type']
            self.types.append(self.prev_type)
            self.ops.append(kargs['op'])

            return self
        else:
            print(f'[Error]: {kargs["op"]} is not a valid method for {self.prev_type}')

    # Any
    def identity(self, ):
        _type, op = self.prev_type, Source.identity.__name__
        self._operation(op=op, var=0, next_type=PSEUDOTYPES.SAME)

    # Array
    # Valid types: ARRAY, MAP, STRING
    def get_float(self, *arg):
        if self.prev_type is TYPES.ARRAY or self.prev_type is TYPES.MAP:
            self._operation(op=Source.get_float.__name__, arg=arg, next_type=TYPES.FLOAT)
        else:
            print(f'[Error]: get_float is not a valid method for {self.prev_type}')
        return self

    # Valid Types: ARRAY, MAP
    def get_map(self, *arg):
        if self.prev_type is TYPES.ARRAY or self.prev_type is TYPES.MAP:
            self._operation(op=Source.get_map.__name__, arg=arg, next_type=TYPES.MAP)
        else:
            print(f'[Error]: get_map is not a valid method for {self.prev_type}')
        return self

    # Valid Types: ARRAY, MAP
    def get_string(self, *arg):
        if self.prev_type is TYPES.ARRAY or self.prev_type is TYPES.MAP:
            self._operation(op=Source.get_string.__name__, arg=arg, next_type=TYPES.STRING)
        else:
            print(f'[Error]: get_string is not a valid method for {self.prev_type}')
        return self

    def map(self, *arg):
        self._operation(op=Source.map.__name__, arg=arg, next_type=PSEUDOTYPES.SUBSCRIPT)
        return self

    def reduce(self, *arg):
        self._operation(op=Source.reduce.__name__, arg=arg, next_type=PSEUDOTYPES.INNER)
        return self

    def some(self, *arg):
        self._operation(op=Source.some.__name__, arg=arg, next_type=TYPES.BOOLEAN)
        return self

    def sort(self, *arg):
        self._operation(op=Source.sort.__name__, arg=arg, next_type=PSEUDOTYPES.SAME)
        return self

    def take(self, *arg):
        self._operation(op=Source.take.__name__, arg=arg, next_type=PSEUDOTYPES.SAME)
        return self

    # BOOLEAN
    # Valid Types: BOOLEAN, BYTES, INTEGER, FLOAT, MAP
    def as_string(self, *arg):
        if self.prev_type is TYPES.BOOLEAN or self.prev_type is TYPES.BYTES or self.prev_type is TYPES.INTEGER or \
                self.prev_type is TYPES.FLOAT or self.prev_type is TYPES.MAP:
            self._operation(op=Source.as_string.__name__, arg=arg, next_type=TYPES.STRING)
        else:
            print(f'[Error]: as_string is not a valid method for {self.prev_type}')
        return self

    # Valid Types: BOOLEAN, INTEGER, STRING
    def match(self, *arg):
        if self.prev_type is TYPES.BOOLEAN or self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.match.__name__, arg=arg, next_type=PSEUDOTYPES.MATCH)
        else:
            print(f'[Error]: match is not a valid method for {self.prev_type}')
        return self

    def negate(self, *arg):
        self._operation(op=Source.negate.__name__, arg=arg, next_type=TYPES.BOOLEAN)
        return self

    # Bytes
    def hash(self, *arg):
        self._operation(op=Source.hash.__name__, arg=arg, next_type=TYPES.BYTES)
        return self

    # Integer
    # Valid Types: INTEGER, FLOAT
    def absolute(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.absolute.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: absolute is not a valid method for {self.prev_type}')
        return self

    def as_float(self, *arg):
        self._operation(op=Source.as_float.__name__, arg=arg, next_type=TYPES.FLOAT)
        return self

    # Valid Types: INTEGER, FLOAT
    def greater_than(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.greater_than.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: greater_than is not a valid method for {self.prev_type}')
        return self

    # Valid Types: INTEGER, FLOAT
    def less_than(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.less_than.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: less_than is not a valid method for {self.prev_type}')
        return self

    # Valid Types: INTEGER, FLOAT
    def modulo(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.modulo.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: modulo is not a valid method for {self.prev_type}')
        return self

    # Valid Types: INTEGER, FLOAT
    def multiply(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.multiply.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(arg)
            print(f'[Error]: multiply is not a valid method for {self.prev_type}')
        return self

    # Valid Types: INTEGER, FLOAT
    def power(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.power.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: power is not a valid method for {self.prev_type}')
        return self

    # Valid Types: INTEGER, FLOAT
    def reciprocal(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.reciprocal.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: reciprocal is not a valid method for {self.prev_type}')
        return self

    # Valid Types: INTEGER, FLOAT
    def sum(self, *arg):
        if self.prev_type is TYPES.INTEGER or self.prev_type is TYPES.FLOAT:
            self._operation(op=Source.sum.__name__, arg=arg, next_type=self.prev_type)
        else:
            print(f'[Error]: sum is not a valid method for {self.prev_type}')
        return self

    # Float
    def ceiling(self, *arg):
        self._operation(op=Source.ceiling.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def floor(self, *arg):
        self._operation(op=Source.floor.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def round(self, *arg):
        self._operation(op=Source.round.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def truncate(self, *arg):
        self._operation(op=Source.truncate.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    # Map
    def entries(self, *arg):
        self._operation(op=Source.entries.__name__, arg=arg, next_type=PSEUDOTYPES.SAME)
        return self

    def get_array(self, *arg):
        self._operation(op=Source.get_array.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def get_boolean(self, *arg):
        self._operation(op=Source.get_boolean.__name__, arg=arg, next_type=TYPES.BOOLEAN)
        return self

    def get_bytes(self, *arg):
        self._operation(op=Source.get_bytes.__name__, arg=arg, next_type=TYPES.BYTES)
        return self

    def get_integer(self, *arg):
        self._operation(op=Source.get_integer.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def keys(self, *arg):
        self._operation(op=Source.keys.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def values_as_array(self, *arg):
        self._operation(op=Source.values_as_array.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def values_as_boolean(self, *arg):
        self._operation(op=Source.values_as_boolean.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def values_as_bytes(self, *arg):
        self._operation(op=Source.values_as_bytes.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def values_as_integer(self, *arg):
        self._operation(op=Source.values_as_integer.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def values_as_float(self, *arg):
        self._operation(op=Source.values_as_float.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def values_as_map(self, *arg):
        self._operation(op=Source.values_as_map.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    def values_as_string(self, *arg):
        self._operation(op=Source.values_as_string.__name__, arg=arg, next_type=TYPES.ARRAY)
        return self

    # String
    def as_boolean(self, *arg):
        self._operation(op=Source.as_boolean.__name__, arg=arg, next_type=TYPES.BOOLEAN)
        return self

    def as_bytes(self, *arg):
        self._operation(op=Source.as_bytes.__name__, arg=arg, next_type=TYPES.BYTES)
        return self

    def as_integer(self, *arg):
        self._operation(op=Source.as_integer.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def length(self, *arg):
        self._operation(op=Source.length.__name__, arg=arg, next_type=TYPES.INTEGER)
        return self

    def parse_array_json(self):
        self.ops.append(Source.parse_array_json.__name__)
        self.prev_type = TYPES.ARRAY
        self.types.append(self.prev_type)
        return self

    def parse_map_json(self):
        self.ops.append(Source.parse_map_json.__name__)
        self.prev_type = TYPES.MAP
        self.types.append(self.prev_type)
        return self

    def parse_xml(self):
        self.ops.append(Source.parse_xml.__name__)
        self.prev_type = TYPES.MAP
        self.types.append(self.prev_type)
        return self

    def to_lower_case(self, *arg):
        self._operation(op=Source.to_lower_case.__name__, arg=arg, next_type=TYPES.STRING)
        return self

    def to_upper_case(self, *arg):
        self._operation(op=Source.to_upper_case.__name__, arg=arg, next_type=TYPES.STRING)
        return self
