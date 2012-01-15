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
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class ListingTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        items.append(SimpleTerm('cl', 'cl', u'Commercial Lease'))
        items.append(SimpleTerm('cs', 'cs', u'Commercial Sale'))
        items.append(SimpleTerm('ll', 'll', u'Land Listing'))
        items.append(SimpleTerm('rl', 'rl', u'Residential Lease'))
        items.append(SimpleTerm('rs', 'rs', u'Residential Sale'))
        return SimpleVocabulary(items)


ListingTypesVocabularyFactory = ListingTypesVocabulary()
