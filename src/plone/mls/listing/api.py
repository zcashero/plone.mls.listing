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
"""MLS API utility methods."""

# python imports
import logging

# zope imports
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from mls.apiclient.client import ListingResource
from mls.apiclient.exceptions import MLSError
from plone.mls.core.interfaces import IMLSSettings
from plone.mls.listing import PRODUCT_NAME


logger = logging.getLogger(PRODUCT_NAME)


def prepare_search_params(data):
    """Prepare search params."""
    params = {}
    if len(data.get('listing_type', ())) > 0:
        # Return comma separated list of listing types
        data['listing_type'] = ','.join(data['listing_type'])
    else:
        data['listing_type'] = None
    for item in data:
        # Remove all None-Type values
        if data[item] is not None:
            params[item] = data[item]
    return params


def search_options(category, lang=None):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IMLSSettings)
    base_url = getattr(settings, 'mls_site', None)
    api_key = getattr(settings, 'mls_key', None)
    resource = ListingResource(base_url, api_key=api_key)
    results = []
    try:
        results = resource.category(category, lang)
    except MLSError, e:
        logger.warn(e)
        return None
    return results


def recent_listings(params={}, batching=True):
    """Return a list of recent MLS listings."""
    search_params = {
        'sort_on': 'created',
        'reverse': '1',
    }
    search_params.update(params)
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IMLSSettings)
    base_url = getattr(settings, 'mls_site', None)
    api_key = getattr(settings, 'mls_key', None)
    batch = None
    results = []
    resource = ListingResource(base_url, api_key=api_key)

    try:
        results, batch = resource.search(search_params)
    except MLSError, e:
        logger.warn(e)

    if batching:
        return results, batch
    return results


def listing_details(listing_id, lang=None):
    """Return detail information for a listing."""
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IMLSSettings)
    base_url = getattr(settings, 'mls_site', None)
    api_key = getattr(settings, 'mls_key', None)
    resource = ListingResource(base_url, api_key=api_key)
    try:
        listing = resource.get(listing_id, lang=lang)
    except MLSError, e:
        logger.warn(e)
        return None
    return listing.get('listing', None)


def search(params={}, batching=True):
    """Search for listings."""
    search_params = {
        'sort_on': 'listing_id',
    }
    search_params.update(params)
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IMLSSettings)
    base_url = getattr(settings, 'mls_site', None)
    api_key = getattr(settings, 'mls_key', None)
    batch = None
    results = []
    resource = ListingResource(base_url, api_key=api_key)

    try:
        results, batch = resource.search(search_params)
    except MLSError, e:
        logger.warn(e)

    if batching:
        return results, batch
    return results
