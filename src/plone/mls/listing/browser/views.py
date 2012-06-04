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
"""Various browser views for listings."""

# zope imports
from plone.memoize.view import memoize
from zope.component import queryMultiAdapter
from zope.interface import implements
from Products.Five import BrowserView
#from zope.publisher.browser import BrowserView

# local imports
from plone.mls.listing.api import listing_details
from plone.mls.listing.browser.interfaces import IListingDetails


class ListingDetails(BrowserView):
    implements(IListingDetails)

    _error = {}
    _data = None
    listing_id = None

    def __init__(self, context, request):
        super(ListingDetails, self).__init__(context, request)
        self.update()

    def update(self):
        self.portal_state = queryMultiAdapter((self.context, self.request),
                                              name='plone_portal_state')
        self._get_data()

    @memoize
    def _get_data(self):
        """Get the remote listing data from the MLS."""
        lang = self.portal_state.language()
        if getattr(self.request, 'listing_id', None) is not None:
            self.listing_id = self.request.listing_id
        else:
            self.listing_id = getattr(self.context, 'listing_id', None)
        if self.listing_id:
            self._data = listing_details(self.listing_id, lang)

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
    def agent_quote(self):
        if self.data is not None:
            return self.data.get('agent_quote', None)

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
