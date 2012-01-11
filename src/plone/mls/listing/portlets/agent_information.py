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
"""Agent Information Portlet."""

# zope imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implements

# local imports
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.i18n import _


class IAgentInformationPortlet(IPortletDataProvider):
    """A portlet displaying agent information for a listing."""


class Assignment(base.Assignment):
    """Agent Information Portlet Assignment."""
    implements(IAgentInformationPortlet)

    title = _(
        u'heading_portlet_agent_information',
        default=u'Agent Information',
    )


class Renderer(base.Renderer):
    """Agent Information Portlet Renderer."""

    render = ViewPageTemplateFile('templates/agent_information.pt')

    @property
    def available(self):
        return IListingDetails.providedBy(self.view) and \
               getattr(self.view, 'listing_id', None) is not None


class AddForm(base.NullAddForm):
    """Add the content immediately, without presenting a form."""

    def create(self):
        return Assignment()
