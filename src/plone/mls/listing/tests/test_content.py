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
"""Test Content Types of plone.mls.listing."""

# python imports
import unittest2 as unittest

# zope imports
from Products.CMFCore.utils import getToolByName

# local imports
from plone.mls.listing.testing import PLONE_MLS_LISTING_INTEGRATION_TESTING


LISTING_TYPE = 'plone.mls.listing.listing'


class TestSetup(unittest.TestCase):
    """Content Test Case for plone.mls.listing."""
    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def test_listing_available(self):
        """Test that the listing content type is available."""
        portal = self.layer['portal']
        portal_types = getToolByName(portal, 'portal_types')
        self.assertTrue(LISTING_TYPE in portal_types)
