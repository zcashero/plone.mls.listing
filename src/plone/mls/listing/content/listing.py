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
"""Dexterity based Listing content type."""

# zope imports
from five import grok
from plone.directives import form
from plone.memoize.view import memoize
from zope import schema
from zope.component import getMultiAdapter

# local imports
from plone.mls.core import config
from plone.mls.core.utils import (get_language, get_listing,
    MLSConnectionError, MLSDataError)
from plone.mls.listing.i18n import _


class IListing(form.Schema):
    """A single MLS Listing."""

    title = schema.TextLine(
        description=_(
            u"help_listing_title",
            default=u"",
        ),
        title=_(
            u"label_listing_title",
            default=u"Title",
        ),
    )

    listing_id = schema.TextLine(
        description=_(
            u"help_listing_listing_id",
            default=u"",
        ),
        title=_(
            u"label_listing_listing_id",
            default=u"MLS Listing ID",
        ),
    )


class View(grok.View):
    grok.context(IListing)
    grok.require('zope2.View')

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self._error = {}
        self._data = None

    def __call__(self):
        self._get_data()
        return super(View, self).__call__()

    @memoize
    def _get_data(self):
        """Get the remote listing data from the MLS."""
        _raw = None
        lang = get_language(self.context)
        if getattr(self.request, 'listing_id', None) is not None:
            listing_id = self.request.listing_id
        else:
            listing_id = self.context.listing_id

        from mls.apiclient.client import ListingResource
        api = ListingResource('http://localhost:8060/mls/', 'IULtjlczY6l5zHZLi6jbGPUUqc2jCvD93kxBbnl1ueA', debug=True)
        _raw = api.get(listing_id, lang=lang)

#         try:
#             _raw = get_listing(listing_id, lang=lang)
#         except (MLSDataError, MLSConnectionError), e:
#             self._error['standard'] = u"This listing is temporary not " \
#                                       u"available. Please try again later."
# 
#             ptools = getMultiAdapter((self.context, self.request),
#                 name=u'plone_tools')
#             ms = ptools.membership()
#             if ms.checkPermission('Modify portal content', self.context):
#                 if e.code in [502, 503, 504]:
#                     pstate = getMultiAdapter((self.context, self.request),
#                         name=u'plone_portal_state')
#                     portal_url = pstate.portal_url()
#                     self._error['extended'] = config.ERROR_503 % dict(
#                         portal_url=portal_url)
# 
#                 elif e.code == 404:
#                     self._error['extended'] = config.ERROR_404

        if _raw is not None:
            self._data = _raw.get('listing', None)

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
