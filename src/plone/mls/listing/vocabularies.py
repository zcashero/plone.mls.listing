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
"""Vocabulary definitions."""

# zope imports
from plone.registry.interfaces import IRegistry

from zope.component import getUtility, queryMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

# local imports
from plone.mls.core.interfaces import IMLSSettings
from plone.mls.listing.api import search_options
from plone.mls.listing.interfaces import IMLSVocabularySettings

ROOM_VALUES = [
    ('--MINVALUE--', 'Min'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    ('--MAXVALUE--', 'Max'),
]


@implementer(IVocabularyFactory)
class BasePriorityVocabulary(object):
    """Vocabulary factory with optional priority list.

    data = [
        ('x1', 'a1'),
        ('x3', 'a3'),
        ('x4', 'a4'),
        ('x2', 'a2'),
        ('x5', 'a5'),
    ]

    priority = ['x5', 'x3']

    data_sorted = [
        ('x5', 'a5'),
        ('x3', 'a3'),
        ('x1', 'a1'),
        ('x2', 'a2'),
        ('x4', 'a4'),
    ]

    def sort_data(data_arg, priority_arg):
        def get_key(item):
            if item[0] in priority_arg:
                return '__%03d' % priority_arg.index(item[0])
            return item[1]

        data_arg.sort(key=get_key)

        print data_arg
        assert data_arg == data_sorted

    sort_data(data, priority)
    """
    priority = ''
    vocabulary_name = None

    def _sort(self, data, priority):
        """Sort list of tuple by keys in priority list or value otherwise."""

        def get_key(item):
            if item[0] in priority:
                return '__0%03d' % priority.index(item[0])
            return '__1%s' % item[1]

        if len(priority) > 0:
            data.sort(key=get_key)
        else:
            data.sort(key=lambda item: item[1])

        return data

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                         name='plone_portal_state')
        registry = getUtility(IRegistry)
        try:
            settings = registry.forInterface(IMLSVocabularySettings,
                                             check=False)
        except KeyError:
            priority_list = []
        else:
            value = getattr(settings, self.priority, '')
            if value is None:
                value = ''
            priority_list = [item.strip() for item in value.split(',') \
                             if len(item.strip()) > 0]

        try:
            global_settings = registry.forInterface(IMLSSettings)
        except KeyError:
            mls_url = None
        else:
            mls_url = getattr(global_settings, 'mls_site', None)

        types = search_options(mls_url, self.vocabulary_name,
                               portal_state.language())
        terms = []
        if types is not None:
            types = self._sort(types, priority_list)
            terms = [SimpleTerm(item[0], item[0], item[1]) for item in types]
        return SimpleVocabulary(terms)


class GeographicTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'geographic_types'."""

    vocabulary_name = 'geographic_types'
    priority = 'geographic_types_priority'

GeographicTypesVocabularyFactory = GeographicTypesVocabulary()


class ListingTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'listing_types'."""

    vocabulary_name = 'listing_types'
    priority = 'listing_types_priority'

ListingTypesVocabularyFactory = ListingTypesVocabulary()


class LocationCountyVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_county'."""

    vocabulary_name = 'location_county'

LocationCountyVocabularyFactory = LocationCountyVocabulary()


class LocationDistrictVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_district'."""

    vocabulary_name = 'location_district'

LocationDistrictVocabularyFactory = LocationDistrictVocabulary()


class LocationStateVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_state'."""

    vocabulary_name = 'location_state'

LocationStateVocabularyFactory = LocationStateVocabulary()


class LocationTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'location_types'."""

    vocabulary_name = 'location_types'
    priority = 'location_types_priority'

LocationTypesVocabularyFactory = LocationTypesVocabulary()


class ObjectTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'object_types'."""

    vocabulary_name = 'object_types'
    priority = 'object_types_priority'

ObjectTypesVocabularyFactory = ObjectTypesVocabulary()


class OwnershipTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'ownership_types'."""

    vocabulary_name = 'ownership_types'
    priority = 'ownership_types_priority'

OwnershipTypesVocabularyFactory = OwnershipTypesVocabulary()


@implementer(IVocabularyFactory)
class RoomsVocabulary(object):

    def __call__(self, context):
        items = []
        for item in ROOM_VALUES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)

RoomsVocabularyFactory = RoomsVocabulary()


class ViewTypesVocabulary(BasePriorityVocabulary):
    """Priority sortable vocabulary factory for 'view_types'."""

    vocabulary_name = 'view_types'
    priority = 'view_types_priority'

ViewTypesVocabularyFactory = ViewTypesVocabulary()


@implementer(IVocabularyFactory)
class YesNoAllVocabulary(object):

    def __call__(self, context):
        items = []
        items.append(SimpleTerm('1', '1', u'Yes'))
        items.append(SimpleTerm('0', '0', u'No'))
        items.append(SimpleTerm('--NOVALUE--', '--NOVALUE--', u'All'))
        return SimpleVocabulary(items)

YesNoAllVocabularyFactory = YesNoAllVocabulary()
