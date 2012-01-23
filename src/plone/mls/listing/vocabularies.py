# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
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
