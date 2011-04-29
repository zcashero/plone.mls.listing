# -*- coding: utf-8 -*-

##############################################################################
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
##############################################################################
"""Test the setup for plone.mls.listing."""

# python imports
import unittest

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase

# local imports
from plone.mls.listing.tests.layer import MLSListingLayer


class SetupTest(PloneTestCase):

    layer = MLSListingLayer

    def afterSetUp(self):
        """Additional setup steps after the test setup is initailized."""

    ###########################################################################
    # Test Product Installations.
    ###########################################################################
    def test_plone_app_dexterity_installed(self):
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'plone.app.dexterity'))

    def test_plone_mls_core_installed(self):
        self.assertTrue(self.portal.portal_quickinstaller.isProductInstalled(
            'plone.mls.core'))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
