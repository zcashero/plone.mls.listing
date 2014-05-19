# -*- coding: utf-8 -*-
"""Test Layer for plone.mls.listing."""

# zope imports
from plone.app.testing import (
    IntegrationTesting,
    PloneSandboxLayer,
    PLONE_FIXTURE,
)
from zope.configuration import xmlconfig


class PloneMLSListing(PloneSandboxLayer):
    """Custom Test Layer for plone.mls.listing."""
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import plone.mls.listing
        xmlconfig.file(
            'configure.zcml',
            plone.mls.listing,
            context=configurationContext,
        )

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        self.applyProfile(portal, 'collective.cover:default')
        self.applyProfile(portal, 'collective.cover:testfixture')
        self.applyProfile(portal, 'plone.mls.listing:default')


PLONE_MLS_LISTING_FIXTURE = PloneMLSListing()
PLONE_MLS_LISTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_MLS_LISTING_FIXTURE, ),
    name='PloneMLSListing:Integration',
)
