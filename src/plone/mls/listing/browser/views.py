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
"""Various stand alone browser views for listings."""

# python imports
from urllib import urlencode

# zope imports
from plone.memoize.view import memoize
from zope.component import queryMultiAdapter
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
from plone.mls.listing.api import recent_listings


class RecentListings(BrowserView):
    """Shows recent (active) listings from the MLS."""

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.limit = int(self.request.get('limit',
                                          getattr(self.context, 'limit', 25)))
        self.portal_state = queryMultiAdapter((self.context, self.request),
                                              name='plone_portal_state')
        self.context_state = queryMultiAdapter((self.context, self.request),
                                               name='plone_context_state')

        self._get_listings()

    @memoize
    def view_url(self):
        if not self.context_state.is_view_template():
            return self.context_state.current_base_url()
        else:
            return absoluteURL(self.context, self.request) + '/'

    @property
    @memoize
    def listings(self):
        return self._listings

    @property
    def batching(self):
        batching = self._batching
        if batching is None:
            return

        page_url = self.context_state.current_base_url()
        limit = self.limit
        offset = int(self.request.get('offset', 0))

        batch = {}
        if batching.get('next', None):
            query = {
                'limit': limit,
                'offset': offset + limit,
            }
            batch.update({
                'next': page_url + '?' + urlencode(query)
            })

        if batching.get('prev', None):
            query = {
                'limit': limit,
                'offset': offset - limit,
            }
            batch.update({
                'prev': page_url + '?' + urlencode(query)
            })
        return batch

    def _get_listings(self):
        """Query the recent listings."""
        params = {
            'limit': self.limit,
            'offset': self.request.get('offset', 0),
            'lang': self.portal_state.language(),
        }
        results, batching = recent_listings(params)
        self._listings = results
        self._batching = batching

    def publishTraverse(self, request, name):
        if getattr(request, 'listing_id', None) is None:
            self.request.listing_id = name
        try:
            return super(RecentListings, self).publishTraverse(request, name)
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
