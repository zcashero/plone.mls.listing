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

#python imports
from email import message_from_string
import re

# zope imports
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as PMF
from plone.app.portlets.portlets import base
from plone.directives import form
from plone.portlets.interfaces import IPortletDataProvider
from plone.z3cform import z2
from z3c.form import button, field
from z3c.form.interfaces import HIDDEN_MODE, IFormLayer
from zope import formlib, schema
from zope.interface import Interface, Invalid, alsoProvides, implementer
from zope.schema.fieldproperty import FieldProperty

# local imports
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.i18n import _

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False


MSG_PORTLET_DESCRIPTION = _(
    u'This portlet shows a form to contact the corresponding agent for a ' \
    u'given listing via email.'
)

EMAIL_TEMPLATE = """\
Enquiry from: %(name)s <%(sender_from_address)s>
Listing URL: %(url)s

Message:
%(message)s
"""

check_email = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}").match


def validate_email(value):
    if not check_email(value):
        raise Invalid(_(u'Invalid email address'))
    return True


class IEmailForm(Interface):
    """Email Form schema."""

    subject = schema.TextLine(
        required=False,
        title=PMF(u'label_subject', default=u'Subject')
    )

    name = schema.TextLine(
        description=PMF(
            u'help_sender_fullname',
            default=u'Please enter your full name',
        ),
        required=True,
        title=PMF(u'label_name', default=u"Name"),
    )

    sender_from_address = schema.TextLine(
        constraint=validate_email,
        description=PMF(
            u'help_sender_from_address',
            default=u'Please enter your e-mail address',
        ),
        required=True,
        title=PMF(u'label_sender_from_address', default=u'E-Mail'),
    )

    message = schema.Text(
        description=PMF(
            u'help_message',
            default=u'Please enter the message you want to send.',
        ),
        max_length=1000,
        required=True,
        title=PMF(u'label_message', default=u'Message'),
    )


class EmailForm(form.Form):
    """Email Form."""
    fields = field.Fields(IEmailForm)
    ignoreContext = True
    method = 'post'
    _email_sent = False

    def __init__(self, context, request, portlet_hash=None, info=None,
                 data=None):
        super(EmailForm, self).__init__(context, request)
        self.listing_info = info
        self.data = data
        if portlet_hash:
            self.prefix = portlet_hash + '.' + self.prefix

    @property
    def already_sent(self):
        return self._email_sent

    def updateWidgets(self):
        super(EmailForm, self).updateWidgets()
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        subject = '%(portal_title)s: %(title)s (%(lid)s)' % dict(
            lid=self.listing_info['listing_id'],
            portal_title=portal.getProperty('title'),
            title=self.listing_info['listing_title'],
        )
        self.widgets['subject'].mode = HIDDEN_MODE
        self.widgets['subject'].value = subject

    @button.buttonAndHandler(PMF(u'label_send', default='Send'), name='send')
    def handle_send(self, action):
        """Send button for sending the email."""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        if not self.already_sent:
            self.send_email(data)
            self._email_sent = True

    def send_email(self, data):
        mailhost = getToolByName(self.context, 'MailHost')
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        # Construct and send a message.
        from_address = portal.getProperty('email_from_address')
        from_name = portal.getProperty('email_from_name')
        if from_name is not None:
            from_address = '%s <%s>' % (from_name, from_address)

        try:
            rcp = self.listing_info['agent'].get('agent_email').get('value')
        except:
            rcp = from_address

        sender = '%s <%s>' % (data['name'], data['sender_from_address'])
        subject = data['subject']
        data['url'] = self.request.getURL()
        message = EMAIL_TEMPLATE % data
        message = message_from_string(message.encode(email_charset))
        message['To'] = rcp
        message['From'] = from_address
        message['Cc'] = sender
        if getattr(self.data, 'bcc', None) is not None:
            message['Bcc'] = self.data.bcc
        message['Reply-to'] = sender
        message['Subject'] = subject

        mailhost.send(message, immediate=True, charset=email_charset)
        return


class IAgentContactPortlet(IPortletDataProvider):
    """A portlet which sends an email to the agent."""

    heading = schema.TextLine(
        description=_(
            u'Custom title for the portlet. If no title is provided, the ' \
            u'default title is used.'),
        required=False,
        title=_(u'Portlet Title'),
    )

    description = schema.Text(
        description=_(u'Additional description for the portlet.'),
        required=False,
        title=_('Description'),
    )

    mail_sent_msg = schema.Text(
        description=_(
            u'Thank you message that is shown after the mail was sent.'
        ),
        required=False,
        title=_(u'Mail Sent Message'),
    )

    bcc = schema.TextLine(
        description=_(
            u'E-mail addresses which receive a blind carbon copy (comma ' \
            u'separated).'),
        required=False,
        title=_(u'BCC Recipients'),
    )


@implementer(IAgentContactPortlet)
class Assignment(base.Assignment):
    """Agent Contact Portlet Assignment."""

    heading = FieldProperty(IAgentContactPortlet['heading'])
    description = FieldProperty(IAgentContactPortlet['description'])
    mail_sent_msg = FieldProperty(IAgentContactPortlet['mail_sent_msg'])
    bcc = FieldProperty(IAgentContactPortlet['bcc'])
    title = _(u'Agent Contact')

    def __init__(self, heading=None, description=None, mail_sent_msg=None,
                 bcc=None):
        self.heading = heading
        self.description = description
        self.mail_sent_msg = mail_sent_msg
        self.bcc = bcc


class Renderer(base.Renderer):
    """Agent Information Portlet Renderer."""

    @property
    def already_sent(self):
        return self.form.already_sent

    @property
    def available(self):
        return IListingDetails.providedBy(self.view) and \
               getattr(self.view, 'listing_id', None) is not None

    @property
    def description(self):
        return self.data.description

    @property
    def mail_sent_msg(self):
        return self.data.mail_sent_msg or PMF(u"Mail sent.")

    @property
    def title(self):
        return self.data.heading or self.data.title

    def update(self):
        listing_info = {
            'listing_id': self.view.info.get('id').get('value'),
            'listing_title': self.view.info.get('title').get('value'),
            'agent': self.view.contact.get('agent'),
        }

        z2.switch_on(self, request_layer=IFormLayer)
        portlet_hash = self.__portlet_metadata__.get('hash')
        self.form = EmailForm(aq_inner(self.context), self.request,
                              portlet_hash, listing_info, self.data)
        if HAS_WRAPPED_FORM:
            alsoProvides(self.form, IWrappedForm)
        self.form.update()


class AddForm(base.AddForm):
    """Add form for the Agent Contact portlet."""
    form_fields = formlib.form.Fields(IAgentContactPortlet)
    label = _(u'Add Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        formlib.form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Edit form for the Agent Contact portlet"""
    form_fields = formlib.form.Fields(IAgentContactPortlet)
    label = _(u'Edit Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION
