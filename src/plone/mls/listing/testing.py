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
"""Test Layer for plone.mls.listing."""

# zope imports
from plone.app.testing import (IntegrationTesting, PloneSandboxLayer,
    PLONE_FIXTURE, applyProfile, quickInstallProduct)
from zope.configuration import xmlconfig


class PloneMLSListing(PloneSandboxLayer):
    """Custom Test Layer for plone.mls.listing."""
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import plone.mls.listing
        xmlconfig.file('configure.zcml', plone.mls.listing,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        applyProfile(portal, 'plone.mls.listing:default')
        quickInstallProduct(portal, 'raptus.article.core')


PLONE_MLS_LISTING_FIXTURE = PloneMLSListing()
PLONE_MLS_LISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_MLS_LISTING_FIXTURE, ),
    name='PloneMLSListing:Integration',
)
