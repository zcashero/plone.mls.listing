# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2012 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESSED OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################
"""Setup for plone.mls.listing package."""

import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('src/'))
from plone.mls.listing import __version__


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
    version=__version__,
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
        "License :: OSI Approved :: Zope Public License",
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
    url='http://pypi.propertyshelf.com/',
    download_url='http://pypi.propertyshelf.com/private/plone.mls.listing',
    license='ZPL 2.1',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.mls'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'plone.app.testing',
            'raptus.article.core',
        ],
    ),
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'Plone',
        'collective.autopermission',
        'collective.prettyphoto',
        'mls.apiclient',
        'plone.app.dexterity [grok]',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.app.versioningbehavior',
        'plone.mls.core',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
