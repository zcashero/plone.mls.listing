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
"""Test Layer for plone.mls.listing."""

# zope imports
from plone.app.testing import (IntegrationTesting, PloneSandboxLayer,
    PLONE_FIXTURE, applyProfile, quickInstallProduct)
from zope.configuration import xmlconfig


class PloneMLSListing(PloneSandboxLayer):
    """Custom Test Layer for plone.mls.listing."""
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import plone.mls.listing
        xmlconfig.file('configure.zcml', plone.mls.listing,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        applyProfile(portal, 'plone.mls.listing:default')
        quickInstallProduct(portal, 'raptus.article.core')


PLONE_MLS_LISTING_FIXTURE = PloneMLSListing()
PLONE_MLS_LISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_MLS_LISTING_FIXTURE, ),
    name='PloneMLSListing:Integration',
)
