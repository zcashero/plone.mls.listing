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
"""MLS Agency Contact Info Settings Control Panel."""

# zope imports
from plone.app.registry.browser import controlpanel

# local imports
from plone.mls.listing.i18n import _
from plone.mls.listing.interfaces import IMLSAgencyContactInformation


class MLSAgencyContactInfoSettingsEditForm(controlpanel.RegistryEditForm):
    """MLS Agency Contact Info Settings Form."""

    schema = IMLSAgencyContactInformation
    label = _(u'')

    def updateFields(self):
        super(MLSAgencyContactInfoSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(MLSAgencyContactInfoSettingsEditForm, self).updateWidgets()


class MLSAgencyContactInfoSettingsControlPanel(
        controlpanel.ControlPanelFormWrapper):
    """MLS Agency Contact Info Settings Control Panel."""

    form = MLSAgencyContactInfoSettingsEditForm
