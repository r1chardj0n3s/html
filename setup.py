#! /usr/bin/env python

from distutils.core import setup

from html.format import __version__, __doc__

import sys
long_description = __doc__
if sys.version_info[0] == 2:
    long_description = long_description.decode('utf8')

# perform the setup action
setup(
    name = "html.format",
    version = __version__,
    description = "simple, elegant HTML, XHTML and XML generation",
    long_description = long_description,
    author = "Richard Jones",
    author_email = "richard@python.org",
    packages = ['html'],
    url = 'http://pypi.python.org/pypi/html.format',
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: BSD License',
    ],
)

# vim: set filetype=python ts=4 sw=4 et si
