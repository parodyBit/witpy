import re
import os
from .system_handler import working_directory
def parse_op(op):
    """

    :param op:
    :return:
    """
    operator = op.split('(')[0]
    var = re.findall('"([^"]*)"', op)
    val = op[op.find("(")+1:op.find(")")]
    if val.isdigit():
        var = int(val)
    return [operator, var]


def valid_url(url):
    """

    :param url:
    :return:
    """
    return re.match(re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE), url)


def snake_to_camel(snake_str):
    """

    :param snake_str:
    :return:
    """
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_to_snake(camel_str):
    """

    :param camel_str:
    :return:
    """
    camel_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str).lower()


def path_to_posix(path=''):
    print(working_directory())
    print(os.path.abspath(path))
    return path

def path_to_nt(path=''):

    print(working_directory())
    print(os.path.split(path))
    return path