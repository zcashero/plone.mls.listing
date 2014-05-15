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
from plone.mls.listing.api import recent_listings

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
    targetpage = schema.TextLine(
        title=_(u'Recent Listings target page'),
        required=False,
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
                    self.data.get('limit', None) or
                    self.data.get('targetpage', None))

    def accepted_ct(self):
        """Return an empty list as no content types are accepted."""
        return []

    @property
    def recent_listings(self):
        self.portal_state = self.context.unrestrictedTraverse("@@plone_portal_state")
        default_limit = 4
        limit = self.data.get('limit', None)

        if limit==None:
            limit = default_limit
        else:
            try:
                #ensure its a number
                limit = int(limit)            
            except:
                #if not - use default
                limit = default_limit
        
        params = {
            'limit': limit,
            'offset': 0,
            'lang': self.portal_state.language(),
        }

        rl_all = recent_listings(params, batching=False)
        #ensure the limit
        rl = rl_all[:limit]

        try:
            for listing in rl:
                listing['lead_image'] = listing['lead_image'].replace("_img_thumb.", "_img.")
            return rl
        except:
            return rl

    @property
    def recent_listings_available(self):
       return len(self.recent_listings) > 0
       
    @property
    def recent_listings_url(self):
        """return the url of the latest listings page"""

        self.portal_state = self.context.unrestrictedTraverse("@@plone_portal_state")
        default_url='/latest-listings'
        url = self.data.get('targetpage', None)

        if url == None:
            url = default_url       
        
        return self.portal_state.navigation_root_url() + url 

