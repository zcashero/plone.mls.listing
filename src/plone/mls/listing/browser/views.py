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
"""Various browser views for listings."""

# python imports
from urllib import urlencode

# zope imports
from Products.CMFPlone.browser.navigation import (get_view_url,
    PhysicalNavigationBreadcrumbs)
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.view import memoize
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
from plone.mls.listing.api import listing_details, recent_listings
from plone.mls.listing.browser.interfaces import IListingDetails


class ListingDetails(BrowserView):
    implements(IListingDetails)

    index = ViewPageTemplateFile('templates/listing_details.pt')

    _error = {}
    _data = None
    listing_id = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        self.portal_state = queryMultiAdapter((self.context, self.request),
                                              name='plone_portal_state')
        self._get_data()

    @memoize
    def _get_data(self):
        """Get the remote listing data from the MLS."""
        lang = self.portal_state.language()
        if getattr(self.request, 'listing_id', None) is not None:
            self.listing_id = self.request.listing_id
        else:
            self.listing_id = getattr(self.context, 'listing_id', None)
        if self.listing_id:
            self._data = listing_details(self.listing_id, lang)

    @property
    def data(self):
        return self._data

    @property
    def error(self):
        return self._error

    @property
    def title(self):
        if getattr(self.request, 'listing_id', None) is not None:
            if self.info is not None:
                title = self.info.get('title', None)
                if title is not None:
                    return title.get('value', self.context.title)
        else:
            return self.context.Title

    @property
    def description(self):
        if self.data is not None:
            return self.data.get('description', None)

    @property
    def long_description(self):
        if self.data is not None:
            return self.data.get('long_description', None)

    @property
    def groups(self):
        if self.data is not None:
            return self.data.get('groups', None)

    @property
    def info(self):
        if self.data is not None:
            return self.data.get('info', None)

    @property
    def lead_image(self):
        if self.data is not None:
            image = self.data.get('images', None)[:1]
            if len(image) > 0:
                return image[0]
        return None

    @property
    def images(self):
        if self.data is not None:
            images = self.data.get('images', None)
            if len(images) > 1:
                return images

    @property
    def contact(self):
        if self.data is not None:
            return self.data.get('contact', None)


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


class ListingNavigationBreadcrumbs(PhysicalNavigationBreadcrumbs):

    def breadcrumbs(self):
        base = super(ListingNavigationBreadcrumbs, self).breadcrumbs()

        name, item_url = get_view_url(self.context)

        listing_id = getattr(self.request, 'listing_id', None)
        if listing_id is not None:
            base += ({'absolute_url': item_url + '/' + listing_id,
                      'Title': listing_id.upper(), },
                    )

        return base
