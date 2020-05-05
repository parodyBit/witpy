from os import path, system
import sys
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from codecs import open


here = path.abspath(path.dirname(__file__))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme_txt = f.read()

with open(path.join(here, 'LICENSE.txt'), encoding='utf-8') as f:
    license_txt = f.read()

about = {}
with open(path.join(here, 'witpy', '__version__.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    system('python setup.py sdist bdist_wheel')
    system('twine upload dist/*')
    sys.exit()
test_requirements = [
    'pytest>=3'
]
packages = ['witpy']
setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme_txt,
    long_description_content_type='text/markdown',
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=license_txt,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ],
    keywords='witnet wallet client json',
    package_dir={'witpy': 'witpy'},
    packages=packages,
    python_requires='>=3.6, <4',
    install_requires=['peppercorn',  # used to convert token stream into data structure html.
                      'apply-defaults',  # Apply default values to functions.
                      'attrs',  # overrides implicit detection in python.
                      'cbor',  # the CBOR library https://cbor.io/
                      'click',  # command line interface tools.
                      'importlib-metadata',  # provides for access to installed package metadata.
                      'jsonschema',  # implementation of JSON Schema for Python.
                      'jsonrpcclient',  # call remote procedures using the JSON-RPC message format.
                      'pyrsistent',  # immutable functional data structures.
                      'six',  # a Python 2 and 3 compatibility library.
                      'websockets',  # WebSocket servers and clients.
                      'zipp',  # A pathlib-compatible Zipfile object wrapper.
                      ],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    extras_require={  # Optional
    },
    project_urls={
        'Bug Reports': 'https://github.com/parodyBit/witpy/issues',
        'Source': 'https://github.com/parodyBit/witpy/',
    },
)



