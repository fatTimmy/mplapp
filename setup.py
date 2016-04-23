"""
mplapp

An GUI toolkit for creating interactive applications with a set of GUI neutral
widgets implemented with Matplotlib artists.

See https://github.com/weegreenblobbie/mplapp
"""
import sys
from setuptools import setup, Extension

# pypi.rst processing

with open("pypi.rst") as fd:
    readme_rst = fd.read()

keywords = '''
    development
'''.split()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Topic :: Utilities",
]

description = """\
An GUI toolkit for creating interactive applications with a set of GUI neutral
widgets implemented with Matplotlib artists.
"""

install_requires = ['matplotlib', 'numpy', 'pyperclip']

if sys.version_info < (3, 0):
    install_requires.append('enum34')

import mplapp

setup(
    author           = mplapp.__author__,
    author_email     = mplapp.__email__,
    classifiers      = classifiers,
    description      = description,
    keywords         = keywords,
    long_description = readme_rst,
    name             = "mplapp",
    package_dir      = {'mplapp' : 'mplapp'},
    packages         = ["mplapp"],
    scripts          = [],
    url              = "https://github.com/weegreenblobbie/mplapp",
    version          = mplapp.__version__,
    install_requires = install_requires,
)
