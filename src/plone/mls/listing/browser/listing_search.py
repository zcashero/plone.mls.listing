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
"""MLS Listing Search."""

# python imports
from urllib import urlencode

# zope imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.memoize.view import memoize
from z3c.form import field, button
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import Interface, alsoProvides, noLongerProvides
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
# from plone.mls.listing.api import recent_listings
from plone.mls.listing.browser.interfaces import (IBaseListingItems, 
    IListingDetails)
from plone.mls.listing.i18n import _

CONFIGURATION_KEY = 'plone.mls.listing.listingsearch'


class IPossibleListingSearch(Interface):
    """Marker interface for possible ListingSearch viewlet."""


class IListingSearch(IBaseListingItems):
    """Marker interface for ListingSearch viewlet."""


class ListingSearchViewlet(ViewletBase):
    """Search for listings in the MLS."""
    index = ViewPageTemplateFile('templates/listing_search_viewlet.pt')

    _listings = None
    _batching = None

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        return IListingSearch.providedBy(self.context) and \
               not IListingDetails.providedBy(self.view)

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


class IListingSearchConfiguration(Interface):
    """Listing Search Configuration Form."""

    limit = schema.Int(
        default=25,
        required=False,
        title=_(
            u"label_listing_search_limit",
            default=u"Items per Page"
        ),
    )


class ListingSearchConfiguration(form.Form):
    """Listing Search Configuration Form."""

    fields = field.Fields(IListingSearchConfiguration)
    label = _(
        u"label_listing_search_configuration",
        default=u"'Listing Search' Configuration",
    )
    description = _(
        u"help_listing_search_configuration",
        default=u"Adjust the behaviour for this 'Listing Search' viewlet.",
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY,
                               annotations.setdefault(CONFIGURATION_KEY, {}))

    def update(self):
        self.request.set('disable_border', True)
        return super(ListingSearchConfiguration, self).update()

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


class ListingSearchStatus(object):
    """Return activation/deactivation status of ListingSearch viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleListingSearch.providedBy(self.context) and \
               not IListingSearch.providedBy(self.context)

    @property
    def active(self):
        return IListingSearch.providedBy(self.context)


class ListingSearchToggle(object):
    """Toggle ListingSearch viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IListingSearch.providedBy(self.context):
            # Deactivate ListingSearch viewlet.
            noLongerProvides(self.context, IListingSearch)
            msg = _(
                u"text_listing_search_deactivated",
                default=u"'Listing Search' viewlet deactivated.",
            )
        elif IPossibleListingSearch.providedBy(self.context):
            alsoProvides(self.context, IListingSearch)
            msg = _(
                u"text_listing_search_activated",
                default=u"'Listing Search' viewlet activated.",
            )
        else:
            msg = _(
                u"text_listing_search_toggle_error",
                default=u"The 'Listing Search' viewlet does't work with " \
                         "this content type. Add 'IPossibleListingSearch' " \
                         "to the provided interfaces to enable this feature.",
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
