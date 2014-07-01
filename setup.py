#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re
import sys


VERSION_FILE = 'placeholder/__init__.py'
version_text = open(VERSION_FILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_text, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError(
        "Unable to find version string in %s." % (VERSION_FILE,))

name = 'django-placeholder'
package = 'placeholder'
description = 'Simple placeholder for django projects'
url = \
    'http://github.com/mauler/django-placeholder'
author = 'Paulo R. Macedo'
author_email = 'proberto.macedo@gmail.com'
license = 'BSD'
install_requires = ['django-classy-tags>=0.4', 'Django']

if sys.argv[-1] == 'publish':
    code = os.system("python setup.py sdist upload")
    if code:
        sys.exit()

    args = {'version': version}
    print "You probably want to also tag the version now:"
    print "  git tag -a %(version)s -m 'version %(version)s'" % args
    print "  git push --tags"
    sys.exit()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name=name,
    version=version,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    packages=find_packages(exclude=('docs', 'example')),
    package_data=get_package_data(package),
    description=description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
    install_requires=install_requires
)
