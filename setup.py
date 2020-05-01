from setuptools import setup, find_packages
from os import path, system

from codecs import open


import sys
here = path.abspath(path.dirname(__file__))

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
    'pytest-httpbin==0.0.7',
    'pytest-cov',
    'pytest-mock',
    'pytest-xdist',
    'PySocks>=1.5.6, !=1.5.7',
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
    tests_require=test_requirements,
    extras_require={  # Optional
    },
    project_urls={
        'Bug Reports': 'https://github.com/parodyBit/witpy/issues',
        'Source': 'https://github.com/parodyBit/witpy/',
    },
)



