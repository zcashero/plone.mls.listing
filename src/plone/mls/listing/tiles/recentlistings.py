# -*- coding: utf-8 -*-
try:
    from collective.cover.tiles.base import IPersistentCoverTile as IPersistentTile
    from collective.cover.tiles.base import PersistentCoverTile as PersistentTile
    USE_COVER = True
except ImportError:
    from plone.tiles import PersistentTile
    from plone.tiles.interfaces import IPersistentTile
    USE_COVER = False

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope import schema
from zope.interface import implementer

from plone.mls.listing.i18n import _

class IRecentListingTile(IPersistentTile):
    """Interface for RecentListing Tile"""
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    limit = schema.Int(
        title=_(u'Limit'),
        required=False,
        default=4
    )

@implementer(IRecentListingTile)
class RecentListingTile(PersistentTile):
    """RecentListing Tile for collective.cover based on a propertyshelf MLS"""
    index = ViewPageTemplateFile('templates/recentlistings.pt')

    is_configurable = True
    is_editable = True
    is_droppable = False

    short_name = _(u'msg_short_name_recentlistings', default=u'Recent Listings')

    def is_empty(self):
        return not( self.data.get('title', None) or
                    self.data.get('limit', None))

    def accepted_ct(self):
        """Return an empty list as no content types are accepted."""
        return []


