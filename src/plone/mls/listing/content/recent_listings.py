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
"""Dexterity based recent listing content type."""

# zope imports
from plone.app.textfield import RichText
from plone.app.textfield.widget import RichTextFieldWidget
from plone.directives import form
from zope import schema

# local imports
from plone.mls.listing.i18n import _


class IRecentListings(form.Schema):
    """Recent Listings Content Type Interface."""

    limit = schema.Int(
        default=25,
        required=True,
        title=_(
            u"label_recent_listings_limit",
            default=u"Items per page"
        ),
    )

    form.widget(body_text=RichTextFieldWidget)
    body_text = RichText(
        required=False,
        title=_(
            u"label_recent_listings_body_text",
            default=u"Body Text",
        ),
    )
