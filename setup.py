from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='witpy',
    version='0.8.0',
    description='A JSON RPC client for the Witnet Protocol.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/parodyBit/witpy/',
    author_email='parody_bit@criptext.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ],
    keywords='witnet wallet client json',
    package_dir={'': 'witpy'},
    packages=find_packages(where='witpy'),
    python_requires='>=3.5, <4',
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
    extras_require={  # Optional
    },
    project_urls={
        'Bug Reports': 'https://github.com/parodyBit/witpy/issues',
        'Source': 'https://github.com/parodyBit/witpy/',
    },
)


