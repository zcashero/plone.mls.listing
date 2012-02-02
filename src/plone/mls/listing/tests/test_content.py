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
