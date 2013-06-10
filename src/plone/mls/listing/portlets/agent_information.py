# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) Propertyshelf, Inc. and its Contributors.
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
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

# local imports
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.i18n import _


MSG_PORTLET_DESCRIPTION = _(
    u'This portlet shows the corresponding agent information for a given '
    u'listing. Note that this portlet is only available for the detail view '
    u'of a listing.'
)


class IAgentInformationPortlet(IPortletDataProvider):
    """A portlet displaying agent information for a listing."""

    heading = schema.TextLine(
        description=_(
            u'Custom title for the portlet. If no title is provided, the '
            u'default title is used.'),
        required=False,
        title=_(u"Portlet Title"),
    )


@implementer(IAgentInformationPortlet)
class Assignment(base.Assignment):
    """Agent Information Portlet Assignment."""

    heading = FieldProperty(IAgentInformationPortlet['heading'])
    title = _(u'Agent Information')

    def __init__(self, heading=None):
        self.heading = heading


class Renderer(base.Renderer):
    """Agent Information Portlet Renderer."""

    @property
    def available(self):
        return IListingDetails.providedBy(self.view) and \
            getattr(self.view, 'listing_id', None) is not None

    @property
    def title(self):
        if self.data.heading is not None:
            return self.data.heading
        return self.data.title


class AddForm(base.AddForm):
    """Add form for the Agent Information portlet."""
    form_fields = form.Fields(IAgentInformationPortlet)
    label = _(u'Add Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Edit form for the Agent Information portlet."""
    form_fields = form.Fields(IAgentInformationPortlet)
    label = _(u'Edit Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION
