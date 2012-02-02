# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2012 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESSED OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

    for item in data:
        if item in ['baths', 'beds', ]:
            min_max = data[item]
            if isinstance(min_max, (list, tuple, )):
                if len(min_max) > 0 and min_max[0] != '--MINVALUE--':
                    params[item + '_min'] = min_max[0]
                if len(min_max) > 1 and min_max[1] != '--MAXVALUE--':
                    params[item + '_max'] = min_max[1]
                continue

        # Convert lists and tuples to comma separated lists.
        if isinstance(data[item], (list, tuple, )):
            if len(data.get(item, ())) > 0:
                data[item] = ','.join(data[item])
            else:
                data[item] = None

        # Remove all None-Type values.
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
