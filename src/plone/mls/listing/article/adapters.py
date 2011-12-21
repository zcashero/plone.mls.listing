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
