# Type names
class TYPES:
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    FLOAT = 'Float'
    STRING = 'String'
    ARRAY = 'Array'
    MAP = 'Map'
    BYTES = 'Bytes'
    RESULT = 'Result'


# Pseudo-type names
class PSEUDOTYPES:
    ANY = 'Any'
    INNER = 'Inner'
    MATCH = 'Match'
    SAME = 'Same'
    SUBSCRIPT = 'Subscript'


class REDUCERS:
    min = 0x00
    max = 0x01
    mode = 0x02
    average_mean = 0x03
    average_mean_weighted = 0x04
    average_median = 0x05
    average_median_weighted = 0x06
    deviation_standard = 0x07
    deviation_average = 0x08
    deviation_median = 0x09
    deviation_maximum = 0x0A


class FILTERS:
    greater_than = 0x00
    less_than = 0x01
    equals = 0x02
    deviation_absolute = 0x03
    deviation_relative = 0x04
    deviation_standard = 0x05
    top = 0x06
    bottom = 0x07
    less_or_equal_than = 0x80
    greater_or_equal_than = 0x81
    not_equals = 0x82
    not_deviation_absolute = 0x83
    not_deviation_relative = 0x84
    not_deviation_standard = 0x85
    not_top = 0x86
    not_bottom = 0x87


type_system = {
    'Any': {
        'identity': [0x00, [PSEUDOTYPES.SAME]],
    },
    'Array': {
        'count': [0x10, [TYPES.INTEGER]],
        'filter': [0x11, [PSEUDOTYPES.SAME]],
        'flatten': [0x12, [PSEUDOTYPES.INNER]],
        'get_array': [0x13, [PSEUDOTYPES.INNER]],
        'get_boolean': [0x14, [TYPES.BOOLEAN]],
        'get_bytes': [0x15, [TYPES.BYTES]],
        'get_float': [0x16, [TYPES.FLOAT]],
        'get_integer': [0x17, [TYPES.INTEGER]],
        'get_map': [0x18, [TYPES.MAP]],
        'get_string': [0x19, [TYPES.STRING]],
        'map': [0x1A, [PSEUDOTYPES.SUBSCRIPT]],
        'reduce': [0x1B, [PSEUDOTYPES.INNER]],
        'some': [0x1C, [TYPES.BOOLEAN]],
        'sort': [0x1D, [PSEUDOTYPES.SAME]],
        'take': [0x1E, [PSEUDOTYPES.SAME]],
    },
    'Boolean': {
        'as_string': [0x20, [TYPES.STRING]],
        'match': [0x21, [PSEUDOTYPES.MATCH]],
        'negate': [0x22, [TYPES.BOOLEAN]]
    },
    'Bytes': {
        'as_string': [0x30, [TYPES.STRING]],
        'hash': [0x31, [TYPES.BYTES]]
    },
    'Integer': {
        'absolute': [0x40, [TYPES.INTEGER]],
        'as_float': [0x41, [TYPES.FLOAT]],
        'as_string': [0x42, [TYPES.STRING]],
        'greater_than': [0x43, [TYPES.BOOLEAN]],
        'less_than': [0x44, [TYPES.BOOLEAN]],
        'match': [0x45, [PSEUDOTYPES.MATCH]],
        'modulo': [0x46, [TYPES.INTEGER]],
        'multiply': [0x47, [TYPES.INTEGER]],
        'negate': [0x48, [TYPES.INTEGER]],
        'power': [0x49, [TYPES.INTEGER]],
        'reciprocal': [0x4A, [TYPES.FLOAT]],
        'sum': [0x4B, [TYPES.INTEGER]],
    },
    'Float': {
        'absolute': [0x50, [TYPES.FLOAT]],
        'asString': [0x51, [TYPES.STRING]],
        'ceiling': [0x52, [TYPES.INTEGER]],
        'greater_than': [0x53, [TYPES.BOOLEAN]],
        'floor': [0x54, [TYPES.INTEGER]],
        'less_than': [0x55, [TYPES.BOOLEAN]],
        'modulo': [0x56, [TYPES.FLOAT]],
        'multiply': [0x57, [TYPES.FLOAT]],
        'negate': [0x58, [TYPES.FLOAT]],
        'power': [0x59, [TYPES.FLOAT]],
        'reciprocal': [0x5A, [TYPES.FLOAT]],
        'round': [0x5B, [TYPES.INTEGER]],
        'sum': [0x5C, [TYPES.FLOAT]],
        'truncate': [0x5d, [TYPES.INTEGER]],
    },
    'Map': {
        # `entries` needs to be deprecated
        'entries': [0x60, [PSEUDOTYPES.SAME]],
        'get_array': [0x61, [TYPES.ARRAY]],
        'get_boolean': [0x62, [TYPES.BOOLEAN]],
        'get_bytes': [0x63, [TYPES.BYTES]],
        'get_float': [0x64, [TYPES.FLOAT]],
        'get_integer': [0x65, [TYPES.INTEGER]],
        'get_map': [0x66, [TYPES.MAP]],
        'get_string': [0x67, [TYPES.STRING]],
        'keys': [0x68, [TYPES.ARRAY, TYPES.STRING]],
        'values_as_array': [0x69, [TYPES.ARRAY, TYPES.ARRAY]],
        'values_as_boolean': [0x6A, [TYPES.ARRAY, TYPES.BOOLEAN]],
        'values_as_bytes': [0x6B, [TYPES.ARRAY, TYPES.BYTES]],
        'values_as_integer': [0x6C, [TYPES.ARRAY, TYPES.INTEGER]],
        'values_as_float': [0x6D, [TYPES.ARRAY, TYPES.FLOAT]],
        'values_as_map': [0x6E, [TYPES.ARRAY, TYPES.MAP]],
        'values_as_string': [0x6F, [TYPES.ARRAY, TYPES.STRING]],
    },
    'String': {
        'as_boolean': [0x70, [TYPES.BOOLEAN]],
        'as_bytes': [0x71, [TYPES.BYTES]],
        'as_float': [0x72, [TYPES.FLOAT]],
        'as_integer': [0x73, [TYPES.INTEGER]],
        'length': [0x74, [TYPES.INTEGER]],
        'match': [0x75, [PSEUDOTYPES.MATCH]],
        'parse_array_json': [0x76, [TYPES.ARRAY]],
        'parse_map_json': [0x77, [TYPES.MAP]],
        'parse_xml': [0x78, [TYPES.MAP]],
        'to_lower_case': [0x79, [TYPES.STRING]],
        'to_upper_case': [0x7A, [TYPES.STRING]],
    }
}
