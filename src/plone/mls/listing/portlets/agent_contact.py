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
"""Agent Contact Portlet."""

# zope imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from zope.interface import implementer

# local imports
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.i18n import _


MSG_PORTLET_DESCRIPTION = _(
    u"This portlet shows a form to contact the corresponding agent for a " \
    u"given listing via email."
)


class IAgentContactPortlet(IPortletDataProvider):
    """A portlet which sends an email to the agent."""


@implementer(IAgentContactPortlet)
class Assignment(base.Assignment):
    """Agent Contact Portlet Assignment."""


class Renderer(base.Renderer):
    """Agent Information Portlet Renderer."""

    render = ViewPageTemplateFile('templates/agent_contact.pt')

    @property
    def available(self):
        return IListingDetails.providedBy(self.view) and \
               getattr(self.view, 'listing_id', None) is not None


class AddForm(base.AddForm):
    """Add the content immediately, without presenting a form."""
    form_fields = form.Fields(IAgentContactPortlet)
    label = _(u"Add Agent Information portlet")
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """"""
    form_fields = form.Fields(IAgentContactPortlet)
    label = _(u"Edit Agent Information portlet")
    description = MSG_PORTLET_DESCRIPTION
