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
from plone.directives import form
from zope import schema

# local imports
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
