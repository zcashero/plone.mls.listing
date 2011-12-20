# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Setup for plone.mls.listing package."""

import os
import sys
from setuptools import setup, find_packages

version = '0.1.2'

#---[ START Server locking]--------------------------------------------------
LOCK_PYPI_SERVER = "http://pypi.propertyshelf.com"


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


def check_server(server):
    if not server:
        return

    COMMANDS_WATCHED = ('register', 'upload')

    changed = False

    for command in COMMANDS_WATCHED:
        if command in sys.argv:
            # Found one command, check for -r or --repository.
            commandpos = sys.argv.index(command)
            i = commandpos + 1
            repo = None
            while i < len(sys.argv) and sys.argv[i].startswith('-'):
                # Check all following options (not commands).
                if (sys.argv[i] == '-r') or (sys.argv[i] == '--repository'):
                    # Next one is the repository itself.
                    try:
                        repo = sys.argv[i + 1]
                        if repo.lower() != server.lower():
                            print "You tried to %s to %s, while this package "\
                                  "is locked to %s" % (command, repo, server)
                            sys.exit(1)
                        else:
                            # Repo is OK.
                            pass
                    except IndexError:
                        # End of args.
                        pass
                i = i + 1

            if repo is None:
                # No repo found for the command.
                print "Adding repository %s to the command %s" % (
                    server, command)
                sys.argv[commandpos + 1: commandpos + 1] = ['-r', server]
                changed = True

    if changed:
        print "Final command: %s" % (' '.join(sys.argv))

check_server(LOCK_PYPI_SERVER)
#---[ END Server locking]----------------------------------------------------

setup(
    name='plone.mls.listing',
    version=version,
    description="Plone support for MLS Listings.",
    long_description='\n\n'.join([
        open("README.txt").read() + "\n" +
        open(os.path.join("docs", "HISTORY.txt")).read(),
    ]),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Intended Audience :: Other Audience",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Zope",
    ],
    keywords='plone zope mls listing',
    author='Thomas Massmann',
    author_email='thomas@propertyshelf.com',
    maintainer='Thomas Massmann',
    maintainer_email='thomas@propertyshelf.com',
    url='http://mypypi.inqbus.de/',
    download_url='http://mypypi.inqbus.de/private/plone.mls.listing',
    license='Commercial',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.mls'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'Plone',
        'plone.app.dexterity [grok]',
        'collective.autopermission',
        'collective.prettyphoto',
        'plone.mls.core',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.app.versioningbehavior',
    ],
    extras_require=dict(
        test=[
            'plone.app.testing',
            'raptus.article.core',
        ],
    ),
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
