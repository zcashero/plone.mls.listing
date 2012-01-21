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
"""MLS Listing collection."""

# zope imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.directives import form
from plone.memoize.view import memoize
from z3c.form import field, button
from z3c.form.browser import checkbox
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import Interface, alsoProvides, noLongerProvides
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
from plone.mls.core.navigation import ListingBatch
from plone.mls.listing.api import prepare_search_params, search
from plone.mls.listing.browser.interfaces import (IBaseListingItems,
    IListingDetails)
from plone.mls.listing.i18n import _


CONFIGURATION_KEY = 'plone.mls.listing.listingcollection'


class IPossibleListingCollection(Interface):
    """Marker interface for possible ListingCollection viewlet."""


class IListingCollection(IBaseListingItems):
    """Marker interface for ListingCollection viewlet."""


class ListingCollectionViewlet(ViewletBase):
    """Dynamic collection of MLS listings."""
    index = ViewPageTemplateFile('templates/listing_collection_viewlet.pt')

    _listings = None
    _batching = None

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        return IListingCollection.providedBy(self.context) and \
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
            'offset': self.request.get('b_start', 0),
            'lang': self.portal_state.language(),
        }
        params.update(self.config)
        params = prepare_search_params(params)
        results, batching = search(params)
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
        return ListingBatch(self.listings, self.limit,
                            self.request.get('b_start', 0), orphan=1,
                            batch_data=self._batching)


class IListingCollectionConfiguration(Interface):
    """Listing Collection Configuration Form."""

    listing_type = schema.Tuple(
        default=('cl', 'cs', 'll', 'rl', 'rs', ),
        required=False,
        title=_(
            u"label_listing_search_listing_type",
            default=u"Listing Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.ListingTypes'
        ),
    )

    location_state = schema.Choice(
        required=False,
        title=u'State',
        source='plone.mls.listing.LocationStates',
    )

    location_county = schema.Choice(
        required=False,
        title=u'County',
        source='plone.mls.listing.LocationCounties',
    )

    location_district = schema.Choice(
        required=False,
        title=u'District',
        source='plone.mls.listing.LocationDistricts',
    )

    price_min = schema.Int(
        required=False,
        title=u'Price (Min)',
    )

    price_max = schema.Int(
        required=False,
        title=u'Price (Max)',
    )

    location_type = schema.Tuple(
        required=False,
        title=_(
            u"label_listing_search_location_type",
            default=u"Location Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.LocationTypes'
        ),
    )

    geographic_type = schema.Tuple(
        required=False,
        title=_(
            u"label_listing_search_geographic_type",
            default=u"Geographic Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.GeographicTypes'
        ),
    )

    view_type = schema.Tuple(
        required=False,
        title=_(
            u"label_listing_search_view_type",
            default=u"View Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.ViewTypes'
        ),
    )

    object_type = schema.Tuple(
        required=False,
        title=_(
            u"label_listing_search_object_type",
            default=u"Object Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.ObjectTypes'
        ),
    )

    ownership_type = schema.Tuple(
        required=False,
        title=_(
            u"label_listing_search_ownership_type",
            default=u"Ownership Type",
        ),
        value_type=schema.Choice(
            source='plone.mls.listing.OwnershipTypes'
        ),
    )

    limit = schema.Int(
        default=25,
        required=False,
        title=_(
            u"label_listing_collection_limit",
            default=u"Items per Page"
        ),
    )


class ListingCollectionConfiguration(form.Form):
    """Listing Collection Configuration Form."""

    fields = field.Fields(IListingCollectionConfiguration)
    fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    label = _(
        u"label_listing_collection_configuration",
        default=u"'Listing Collection' Configuration",
    )
    description = _(
        u"help_listing_collection_configuration",
        default=u"Adjust the behaviour for this 'Listing Collection' viewlet.",
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY,
                               annotations.setdefault(CONFIGURATION_KEY, {}))

    @button.buttonAndHandler(_(u"Save"))
    def handle_save(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        annotations = IAnnotations(self.context)
        annotations[CONFIGURATION_KEY] = data
        self.request.response.redirect(absoluteURL(self.context, self.request))

    @button.buttonAndHandler(_(u"Cancel"))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))


class ListingCollectionStatus(object):
    """Return activation/deactivation status of ListingCollection viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleListingCollection.providedBy(self.context) and \
               not IListingCollection.providedBy(self.context)

    @property
    def active(self):
        return IListingCollection.providedBy(self.context)


class ListingCollectionToggle(object):
    """Toggle ListingCollection viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IListingCollection.providedBy(self.context):
            # Deactivate ListingCollection viewlet.
            noLongerProvides(self.context, IListingCollection)
            msg = _(
                u"text_listing_collection_deactivated",
                default=u"'Listing Collection' viewlet deactivated.",
            )
        elif IPossibleListingCollection.providedBy(self.context):
            alsoProvides(self.context, IListingCollection)
            msg = _(
                u"text_listing_collection_activated",
                default=u"'Listing Collection' viewlet activated.",
            )
        else:
            msg = _(
                u"text_listing_collection_toggle_error",
                default=u"The 'Listing Collection' viewlet does't work with " \
                         "this content type. Add " \
                         "'IPossibleListingCollection' to the provided " \
                         "interfaces to enable this feature.",
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
