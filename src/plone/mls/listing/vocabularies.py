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
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

# local imports
from plone.mls.listing.api import search_options


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


class GeographicTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('geographic_types', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


GeographicTypesVocabularyFactory = GeographicTypesVocabulary()


class ListingTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('listing_types', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


ListingTypesVocabularyFactory = ListingTypesVocabulary()


class LocationCountyVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('location_county', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


LocationCountyVocabularyFactory = LocationCountyVocabulary()


class LocationDistrictVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('location_district', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


LocationDistrictVocabularyFactory = LocationDistrictVocabulary()


class LocationStateVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('location_state', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


LocationStateVocabularyFactory = LocationStateVocabulary()


class LocationTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('location_types', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


LocationTypesVocabularyFactory = LocationTypesVocabulary()


class ObjectTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('object_types', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


ObjectTypesVocabularyFactory = ObjectTypesVocabulary()


class OwnershipTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('ownership_types', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


OwnershipTypesVocabularyFactory = OwnershipTypesVocabulary()


class RoomsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        for item in ROOM_VALUES:
            items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


RoomsVocabularyFactory = RoomsVocabulary()


class ViewTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_state = queryMultiAdapter((context, getRequest()),
                                          name='plone_portal_state')

        types = search_options('view_types', portal_state.language())
        items = []
        if types is not None:
            for item in types:
                items.append(SimpleTerm(item[0], item[0], item[1]))
        return SimpleVocabulary(items)


ViewTypesVocabularyFactory = ViewTypesVocabulary()


class YesNoAllVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        items.append(SimpleTerm('1', '1', u'Yes'))
        items.append(SimpleTerm('0', '0', u'No'))
        items.append(SimpleTerm('--NOVALUE--', '--NOVALUE--', u'All'))
        return SimpleVocabulary(items)


YesNoAllVocabularyFactory = YesNoAllVocabulary()