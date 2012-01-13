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
"""Custom Traverser implementation for IRecentListings."""

# zope imports
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import queryMultiAdapter
from zope.publisher.interfaces import NotFound


class RecentListingsTraverser(DefaultPublishTraverse):
    """Custom Traverser for IRecentListings."""

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""
        # Try to deliver the default content views.
        try:
            return super(RecentListingsTraverser, self).publishTraverse(
                request, name)
        except (NotFound, AttributeError):

            # We store the listing_id parameter in the request.
            self.request.listing_id = name
            listing_view = 'listing-detail'
            default_view = self.context.getDefaultLayout()

            # Let's call the listing view.
            view = queryMultiAdapter((self.context, request),
                                     name=listing_view)
            if view is not None:
                return view

            # Deliver the default item view as fallback.
            view = queryMultiAdapter((self.context, request),
                                     name=default_view)
            if view is not None:
                return view

        raise NotFound(self.context, name, request)
