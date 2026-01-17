# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

import re
from io import open

from setuptools import find_packages, setup

PACKAGE_NAME = "num2words2"

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Topic :: Software Development :: Internationalization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Localization',
    'Topic :: Text Processing :: Linguistic',
]

LONG_DESC = open('README.rst', 'rt', encoding="utf-8").read() + '\n\n' + \
            open('CHANGES.rst', 'rt', encoding="utf-8").read()


def find_version(fname):
    """Parse file & return version number matching 0.0.1 regex
    Returns str or raises RuntimeError
    """
    version = ''
    with open(fname, 'r', encoding="utf-8") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


setup(
    name=PACKAGE_NAME,
    version=find_version("bin/num2words2"),
    description='Modern, actively maintained fork of num2words optimized for LLM/AI/speech applications.',
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    license='LGPL',
    author='Jean-Louis Queguiner',
    author_email='jean-louis.queguiner@gmail.com',
    maintainer='Jean-Louis Queguiner',
    maintainer_email='jean-louis.queguiner@gmail.com',
    keywords=' number word numbers words convert conversion i18n '
             'localisation localization internationalisation '
             'internationalization',
    url='https://github.com/jqueguiner/num2words',
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    classifiers=CLASSIFIERS,
    scripts=['bin/num2words2'],
    install_requires=["docopt>=0.6.2"],
    tests_require=['delegator.py'],
)
