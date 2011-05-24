# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, LLC and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
###############################################################################
"""This is an integration "unit" test.

It uses PloneTestCase, but does not use doctest syntax. You will find lots of
examples of this type of test in CMFPlone/tests, for example.
"""

# python imports
import unittest

# zope imports
from Products.CMFCore.utils import getToolByName
from plone.browserlayer import utils as layerutils

# local imports
from plone.mls.listing.tests.base import ProductTestCase

LISTING_TYPE = 'plone.mls.listing.listing'


class TestSetup(ProductTestCase):
    """Product Test Setup."""

    def afterSetUp(self):
        """Additional setup steps after the test setup is initialized."""
        self.portal_types = getToolByName(self.portal, 'portal_types')
        self.portal_repo = getToolByName(self.portal, 'portal_repository')

    ###########################################################################
    # Test Product Installations.
    ###########################################################################
    def test_plone_app_dexterity_installed(self):
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'plone.app.dexterity'))

    def test_plone_mls_core_installed(self):
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'plone.mls.core'))

    def test_raptus_article_core_installed(self):
        # raptus.article.core will be installed only on tests.
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'raptus.article.core'))

    ###########################################################################
    # Test Content Type.
    ###########################################################################
    def test_listing_available(self):
        listing = self.portal_types.get(LISTING_TYPE, None)
        self.failUnless(listing is not None)

    def test_versioning(self):
        versionable_types = list(self.portal_repo.getVersionableContentTypes())
        self.failUnless(LISTING_TYPE in versionable_types)

    def test_article_integration(self):
        article = self.portal_types.get('Article', None)
        self.failUnless(article is not None)
        self.failUnless(LISTING_TYPE in article.allowed_content_types)


def test_suite():
    """This sets up a test suite that runs the tests in the class above."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
