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
"""Article Provider."""

# zope imports
from Products.CMFCore.utils import getToolByName
from raptus.article.core.interfaces import IArticle
from zope.component import adapts
from zope.interface import implements


# local imports
from plone.mls.listing.article.interfaces import IListingLists


class ListingLists(object):
    """Provider for listings contained in an article."""
    implements(IListingLists)
    adapts(IArticle)
    
    def __init__(self, context):
        self.context = context
        
    def getListingLists(self, **kwargs):
        """Returns a list of listings (catalog brains)."""
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(
            portal_type='plone.mls.listing.listing',
            path={
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1,
            },
            sort_on='getObjPositionInParent', **kwargs)
