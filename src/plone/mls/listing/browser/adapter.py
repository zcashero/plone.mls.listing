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
"""View adapter."""

# plone imports
from z3c.form.widget import StaticWidgetAttribute

# local imports
from plone.mls.listing import browser
from plone.mls.listing.i18n import _

PleaseSelectLCC = StaticWidgetAttribute(_(u"All"),
    view=browser.listing_collection.ListingCollectionConfiguration)
PleaseSelectLSF = StaticWidgetAttribute(_(u"All"),
    view=browser.listing_search.ListingSearchForm)
PleaseSelectRLC = StaticWidgetAttribute(_(u"All"),
    view=browser.recent_listings.RecentListingsConfiguration)


PleaseSelectState = StaticWidgetAttribute(_(u'All'),
    field=browser.listing_search.IListingSearchForm['location_state'])
PleaseSelectCounty = StaticWidgetAttribute(_(u'All'),
    field=browser.listing_search.IListingSearchForm['location_county'])
PleaseSelectDistrict = StaticWidgetAttribute(_(u'All'),
    field=browser.listing_search.IListingSearchForm['location_district'])
