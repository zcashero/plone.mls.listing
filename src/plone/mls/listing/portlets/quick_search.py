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
from Acquisition import aq_inner
from plone.app.portlets.portlets import base
from plone.directives import form
from plone.portlets.interfaces import IPortletDataProvider
from plone.z3cform import z2
from z3c.form import field
from z3c.form.browser import checkbox, radio
from z3c.form.interfaces import IFormLayer
from zope import formlib, schema
from zope.interface import alsoProvides, implementer
from zope.schema.fieldproperty import FieldProperty

# local imports
from plone.mls.listing.browser.listing_search import IListingSearchForm
from plone.mls.listing.browser.valuerange.widget import ValueRangeFieldWidget
from plone.mls.listing.i18n import _

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False


MSG_PORTLET_DESCRIPTION = _(u'This portlet shows a listing quick search form.')


class QuickSearchForm(form.Form):
    """Quick Search Form."""
    fields = field.Fields(IListingSearchForm)
    ignoreContext = True

    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['baths'].widgetFactory = ValueRangeFieldWidget
    fields['beds'].widgetFactory = ValueRangeFieldWidget
    #additional fields for filtering
    fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget

    fields['air_condition'].widgetFactory = radio.RadioFieldWidget
    fields['jacuzzi'].widgetFactory = radio.RadioFieldWidget
    fields['pool'].widgetFactory = radio.RadioFieldWidget

    def __init__(self, context, request, portlet_hash=None, data=None):
        super(QuickSearchForm, self).__init__(context, request)
        self.data = data
        if portlet_hash:
            self.prefix = portlet_hash + '.' + self.prefix


class IQuickSearchPortlet(IPortletDataProvider):
    """A portlet displaying a listing quick search form."""

    heading = schema.TextLine(
        description=_(
            u'Custom title for the portlet. If no title is provided, the ' \
            u'default title is used.'),
        required=False,
        title=_(u"Portlet Title"),
    )


@implementer(IQuickSearchPortlet)
class Assignment(base.Assignment):
    """Quick Search Portlet Assignment."""

    heading = FieldProperty(IQuickSearchPortlet['heading'])
    title = _(u'Listing Search')

    def __init__(self, heading=None):
        self.heading = heading


class Renderer(base.Renderer):
    """Agent Information Portlet Renderer."""

    @property
    def title(self):
        if self.data.heading is not None:
            return self.data.heading
        return self.data.title

    def update(self):
        z2.switch_on(self, request_layer=IFormLayer)
        portlet_hash = self.__portlet_metadata__.get('hash')
        self.form = QuickSearchForm(aq_inner(self.context), self.request,
                              portlet_hash)
        if HAS_WRAPPED_FORM:
            alsoProvides(self.form, IWrappedForm)
        self.form.update()


class AddForm(base.AddForm):
    """Add form for the Agent Information portlet."""
    form_fields = formlib.form.Fields(IQuickSearchPortlet)
    label = _(u'Add Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        formlib.form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Edit form for the Agent Information portlet."""
    form_fields = formlib.form.Fields(IQuickSearchPortlet)
    label = _(u'Edit Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION
