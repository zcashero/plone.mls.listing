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
"""Navigation Breadcrumb customizations."""

# zope imports
from Products.CMFPlone.browser.navigation import (get_view_url,
    PhysicalNavigationBreadcrumbs)


class ListingDetailsNavigationBreadcrumbs(PhysicalNavigationBreadcrumbs):
    """Custom breadcrumb navigation for listing details."""

    def breadcrumbs(self):
        base = super(ListingDetailsNavigationBreadcrumbs, self).breadcrumbs()

        name, item_url = get_view_url(self.context)

        listing_id = getattr(self.request, 'listing_id', None)
        last_item = self.request.steps[-2:-1]
        if listing_id is not None and self.context.id in last_item:
            base += ({'absolute_url': item_url + '/' + listing_id,
                      'Title': listing_id.upper(), },
                    )

        return base
