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
"""Interface definitions."""

# zope imports
from five import grok
from plone.directives import form
from zope import schema

# local imports
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
    
