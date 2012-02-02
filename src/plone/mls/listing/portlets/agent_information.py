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
