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
"""Recent MLS Listings."""

# python imports
from urllib import urlencode

# zope imports
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.directives import form
from plone.memoize.view import memoize
from z3c.form import field, button
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import Interface, implements
from zope.publisher.browser import BrowserView
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
from plone.mls.listing.api import recent_listings
from plone.mls.listing.i18n import _

CONFIGURATION_KEY = 'plone.mls.listing.recentlistings'


class IRecentListings(Interface):
    """Marker interface for RecentListings view."""


class RecentListings(BrowserView):
    """Show recent MLS listings."""
    implements(IRecentListings)

    def __call__(self):
        self.update()
        return self.index()

    @property
    def config(self):
        """Get view configuration data from annotations."""
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY, {})

    def update(self):
        """Prepare view related data."""
        self.portal_state = queryMultiAdapter((self.context, self.request),
                                              name='plone_portal_state')
        self.context_state = queryMultiAdapter((self.context, self.request),
                                               name='plone_context_state')

        self.limit = self.config.get('limit', 25)
        self._get_listings()

    def _get_listings(self):
        """Query the recent listings from the MLS."""
        params = {
            'limit': self.limit,
            'offset': self.request.get('offset', 0),
            'lang': self.portal_state.language(),
        }
        results, batching = recent_listings(params)
        self._listings = results
        self._batching = batching

    @property
    @memoize
    def listings(self):
        """Return listing results."""
        return self._listings

    @memoize
    def view_url(self):
        """Generate view url."""
        if not self.context_state.is_view_template():
            return self.context_state.current_base_url()
        else:
            return absoluteURL(self.context, self.request) + '/'

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
                'offset': offset + limit,
            }
            batch.update({
                'next': page_url + '?' + urlencode(query)
            })

        if batching.get('prev', None):
            query = {
                'offset': offset - limit,
            }
            batch.update({
                'prev': page_url + '?' + urlencode(query)
            })
        return batch


class IRecentListingsConfiguration(Interface):
    """Recent Listings Configuration Form."""

    listing_type = schema.List(
        default=None,
        required=False,
        title=_(
            u"label_recent_listings_listing_types",
            default=u"Listing Types"
        ),
        value_type=schema.Choice(
            values=['Residential Lease', 'Residential Sale'],
        ),
    )

    price_min = schema.Int(
        description=_(
            u"help_recent_listings_price_min",
            default=u"Enter the minimum price for listings. If no price is " \
                     "given, all listings from the lowest price are shown.",
        ),
        required=False,
        title=_(
            u"label_recent_listings_price_min",
            default=u"Minimum Price",
        ),
    )

    price_max = schema.Int(
        description=_(
            u"help_recent_listings_price_max",
            default=u"Enter the maximum price for listings. If no price is " \
                     "given, all listings to the highest price are shown.",
        ),
        required=False,
        title=_(
            u"label_recent_listings_price_max",
            default=u"Maximum Price",
        ),
    )

    limit = schema.Int(
        default=25,
        required=False,
        title=_(
            u"label_recent_listings_limit",
            default=u"Items per Page"
        ),
    )


class RecentListingsConfiguration(form.Form):
    """Recent Listings Configuration Form."""

    fields = field.Fields(IRecentListingsConfiguration)
    label = _(
        u"label_recent_listings_configuration",
        default=u"'Recent Listings' Configuration",
    )
    description = _(
        u"help_recent_listings_configuration",
        default=u"Adjust the behaviour for this 'Recent Listings' view.",
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY,
                               annotations.setdefault(CONFIGURATION_KEY, {}))

    def update(self):
        self.request.set('disable_border', True)
        return super(RecentListingsConfiguration, self).update()

    @button.buttonAndHandler(_(u"Save"))
    def handle_save(self, action):
        data, errors = self.extractData()
        if not errors:
            annotations = IAnnotations(self.context)
            annotations[CONFIGURATION_KEY] = data
            self.request.response.redirect(absoluteURL(self.context,
                                                       self.request))

    @button.buttonAndHandler(_(u"Cancel"))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))
