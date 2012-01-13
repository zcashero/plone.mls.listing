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
