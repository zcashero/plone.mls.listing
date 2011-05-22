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
"""Setup handlers for plone.mls.listing."""

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import getUtility

LISTING_TYPE = 'plone.mls.listing.listing'


def setup_kupu(context):
    """Set up Kupu."""
    if not context.readDataFile('plone.mls.listing_various.txt'):
        return

    site = getUtility(IPloneSiteRoot)

    portal_types = getToolByName(site, 'portal_types')
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        linkable = list(kupu.getPortalTypesForResourceType('linkable'))
        if LISTING_TYPE not in linkable:
            # Kupu's resource list can accumulate old, no longer valid types.
            # It will throw an exception if we try to resave them.
            # So, let's clean the list.
            valid_types = dict([ (t.id, 1) for t in portal_types.listTypeInfo()])
            linkable = [pt for pt in linkable if pt in valid_types]

            linkable.append(LISTING_TYPE)
            kupu.updateResourceTypes(({
                'resource_type': 'linkable',
                'old_type': 'linkable',
                'portal_types': linkable,
            },))


def setup_article(context):
    """Set up raptus.article."""
    if not context.readDataFile('plone.mls.listing_various.txt'):
        return

    site = getUtility(IPloneSiteRoot)
    quickinstaller = getToolByName(site, 'portal_quickinstaller')
    portal_types = getToolByName(site, 'portal_types')
    if quickinstaller.isProductInstalled('raptus.article.core'):
        article = portal_types.get('Article', None)
        if article is None:
            return
        if not LISTING_TYPE in article.allowed_content_types:
            article.allowed_content_types += (LISTING_TYPE, )
