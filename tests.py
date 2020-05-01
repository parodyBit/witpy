import pytest
from witpy.util.string import camel_to_snake, snake_to_camel


def test_camel_to_snake():
    assert camel_to_snake('camelCase()') == 'camel_case()'

def test_snake_to_camel():
    assert snake_to_camel('snake_case()') == 'snakeCase()'
