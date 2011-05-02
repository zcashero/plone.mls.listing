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
"""Listing content type."""

# zope imports
from five import grok
from plone.directives import form
from plone.memoize.view import memoize
from zope import schema
from zope.publisher.interfaces import NotFound

# local imports
from plone.mls.core.utils import authenticate, get_listing
from plone.mls.listing import _


class IListing(form.Schema):
    """A single MLS Listing."""

    title = schema.TextLine(
        description=_(
            u"help_listing_title",
            default=u"",
        ),
        title = _(
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
        

    @property
    @memoize
    def available(self):
        return authenticate()

    @property
    @memoize
    def raw(self):
        raw = get_listing(self.context.listing_id)
        if not raw:
            raise NotFound(self.context, self.context.listing_id, self.request)
        return raw

    @property
    @memoize
    def data(self):
        return self.raw.get('data', None)

    @property
    @memoize
    def groups(self):
        if self.data is not None:
            return self.data.get('groups', None)
