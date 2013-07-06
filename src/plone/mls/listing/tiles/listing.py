# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try:
    from collective.cover.tiles.base import IPersistentCoverTile as IPersistentTile
    from collective.cover.tiles.base import PersistentCoverTile as PersistentTile
    USE_COVER = True
except ImportError:
    from plone.tiles import PersistentTile
    from plone.tiles.interfaces import IPersistentTile
    USE_COVER = False
from plone.memoize import view
from plone.memoize.instance import memoizedproperty
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.interface import implementer

from plone.mls.listing.i18n import _


class IListingTile(IPersistentTile):
    """"""
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    uuid = schema.TextLine(
        title=_(u'UUID'),
        required=False,
        readonly=True,
    )


@implementer(IListingTile)
class ListingTile(PersistentTile):
    """"""
    index = ViewPageTemplateFile('templates/listing.pt')

    @memoizedproperty
    def brain(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        uuid = self.data.get('uuid')
        result = catalog(UID=uuid) if uuid is not None else []
        assert len(result) <= 1
        return result[0] if result else None

    def is_empty(self):
        return self.brain is None and \
            not [i for i in self.data.values() if i]

    def title(self):
        """ Return the title of the original image
        """
        if self.brain is not None:
            return self.brain.Title

    def populate_with_object(self, obj):
        # check permissions
        super(ListingTile, self).populate_with_object(obj)

        data = {
            'uuid': IUUID(obj, None),  # XXX: can we get None here? see below
        }

        # TODO: if a Dexterity object does not have the IReferenceable
        # behaviour enable then it will not work here
        # we need to figure out how to enforce the use of
        # plone.app.referenceablebehavior
        data_mgr = ITileDataManager(self)
        data_mgr.set(data)

    @view.memoize
    def accepted_ct(self):
        return ['plone.mls.listing.listing', ]
