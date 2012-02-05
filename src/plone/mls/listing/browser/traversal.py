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
"""Custom Traverser implementation for IRecentListings."""

# zope imports
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import queryMultiAdapter
from zope.publisher.interfaces import NotFound


class RecentListingsTraverser(DefaultPublishTraverse):
    """Custom Traverser for IRecentListings."""

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""
        # Try to deliver the default content views.
        try:
            return super(RecentListingsTraverser, self).publishTraverse(
                request, name)
        except (NotFound, AttributeError):

            # We store the listing_id parameter in the request.
            self.request.listing_id = name
            listing_view = 'listing-detail'
            default_view = self.context.getDefaultLayout()

            # Let's call the listing view.
            view = queryMultiAdapter((self.context, request),
                                     name=listing_view)
            if view is not None:
                return view

            # Deliver the default item view as fallback.
            view = queryMultiAdapter((self.context, request),
                                     name=default_view)
            if view is not None:
                return view

        raise NotFound(self.context, name, request)
