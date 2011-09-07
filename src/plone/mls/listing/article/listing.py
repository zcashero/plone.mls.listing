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
"""Article integration for MLS Listings."""

# zope imports
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from zope import interface, component

# raptus.article imports
from raptus.article.core.config import MANAGE_PERMISSION
from raptus.article.core import interfaces
from raptus.article.nesting.interfaces import IArticles

# local imports
from plone.mls.core.utils import (get_language, get_listing, MLSConnectionError,
    MLSDataError)
from plone.mls.listing import _
from plone.mls.listing.article.interfaces import IListingLists


class IListings(interface.Interface):
    """Marker interface for the listings viewlet."""


class ListingsComponent(object):
    """Component which lists the MLS Listings."""
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)
    
    title = _(
        u"heading_article_listings",
        default=u"MLS Listings",
    )
    description = _(
        u"help_article_listings",
        default=u"List of the contained MLS Listings.",
    )
    image = '++resource++listing_left.gif'
    interface = IListings
    viewlet = 'plone.mls.listing.article.listings'
    
    def __init__(self, context):
        self.context = context


class ListingsViewlet(ViewletBase):
    """Viewlet listing the MLS Listings."""
    index = ViewPageTemplateFile('listing.pt')
    image_class = "component componentLeft"
    type = "left"
    thumb_size = "listingleft"
    component = "listing.left"
    
    def _class(self, brain, i, l):
        cls = []
        if i == 0:
            cls.append('first')
        if i == l-1:
            cls.append('last')
        if i % 2 == 0:
            cls.append('odd')
        if i % 2 == 1:
            cls.append('even')
        return ' '.join(cls)
    
    @property
    def title_pre(self):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('listings_%s_titletop' % self.type, False)
    
    @property
    @memoize
    def show_caption(self):
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('listings_%s_caption' % self.type, False)
    
    @property
    @memoize
    def listings(self):
        provider = IListingLists(self.context)
        manageable = interfaces.IManageable(self.context)
#         mship = getToolByName(self.context, 'portal_membership')
#         if mship.checkPermission(MANAGE_PERMISSION, self.context):
#             items = provider.getListingLists()
#         else:
#             items = provider.getListingLists(component=self.component)
        items = provider.getListingLists()
        items = manageable.getList(items)
        i = 0
        l = len(items)

        for item in items:
            item.update({
                'title': item['brain'].Title,
                'description': item['brain'].Description,
                'url': item['brain'].getURL(),
                'class': self._class(item['brain'], i, l),
            })
#             if item.has_key('show') and item['show']:
#                 item['class'] += ' hidden'

            # Use brains instead!
            obj = item['brain'].getObject()
            listing_id = obj.listing_id
            lang = get_language(obj)
            try:
                raw = get_listing(listing_id, summary=True, lang=lang)
            except (MLSDataError, MLSConnectionError), e:
                continue
            else:
                listing = raw.get('listing', None)
                item['listing'] = listing

            i += 1
        return items
