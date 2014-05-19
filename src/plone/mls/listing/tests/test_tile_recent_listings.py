# -*- coding: utf-8 -*-
"""Integration tests for the 'Recent Listings' tile."""

# python imports
from mock import Mock
import unittest2 as unittest

# zope imports
from collective.cover.tests.base import TestTileMixin

# local imports
from plone.mls.listing.testing import PLONE_MLS_LISTING_INTEGRATION_TESTING
from plone.mls.listing.tiles.recentlistings import (
    IRecentListingTile,
    RecentListingTile,
)


class TileRecentListingsTestCase(TestTileMixin, unittest.TestCase):

    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def setUp(self):
        super(TileRecentListingsTestCase, self).setUp()
        self.tile = RecentListingTile(self.cover, self.request)
        self.tile.__name__ = u'plone.mls.listing.recentlistings'
        self.tile.id = u'test'

    @unittest.expectedFailure
    def test_interface(self):
        self.interface = IRecentListingTile
        self.klass = RecentListingTile
        super(TileRecentListingsTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertFalse(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), [])

    def test_tile_is_empty(self):
        self.assertTrue(self.tile.is_empty())

    def test_render_empty(self):
        msg = u'Edit the title of this tile and change the its configuration.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())
