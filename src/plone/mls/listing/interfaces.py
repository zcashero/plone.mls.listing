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
"""Propertyshelf MLS Embedding interfaces."""

# zope imports
from zope import schema
from zope.interface import Interface

# local imports
from plone.mls.listing.i18n import _

MSG_PRIORITY_DESCRIPTION = _(
    u'Items in this vocabulary are sorted by priority key (if available) ' \
    u'and value otherwise.Enter one item per line. Possible values are: %s'
)

POSSIBLE_GEOGRAPHIC_TYPES = ', '.join([
    'cloud_forest', 'dry_forest', 'highland_forest', 'rain_forest',
    'swamp_forest',
])

POSSIBLE_LISTING_TYPES = ', '.join(['cl', 'cs', 'll', 'rl', 'rs', ])

POSSIBLE_LOCATION_TYPES = ', '.join([
    'lakefront', 'mountain', 'oceanfront', 'oceanvicinity', 'riverfront',
    'rural', 'urban',
])

POSSIBLE_OBJECT_TYPES = ', '.join([
    'agricultural_land', 'apartment', 'bar_nightclub', 'commercial_condo',
    'condominium', 'construction_site', 'development_land',
    'freestanding_building', 'freestanding_villa', 'half_duplex',
    'hotel_hostel', 'house', 'medical_facility', 'mixed_use_building',
    'multi_unit_building', 'multiplex', 'office_condo', 'protected_area',
    'restaurant', 'retail_singleplex', 'strip_center_complex',
    'strip_center_unit', 'townhouse', 'warehouse',
])

POSSIBLE_OWNERSHIP_TYPES = ', '.join([
    'bank_owned', 'concession', 'fee_simple', 'fractional',
])

POSSIBLE_VIEW_TYPES = ', '.join([
    'bay_view', 'beach_view', 'city_view', 'eastern_view', 'garden_view',
    'greenbelt_view', 'lake_view', 'mountain_view', 'northern_view',
    'ocean_view', 'pond_view', 'river_view', 'southern_view', 'valley_view',
    'western_view', 'wooded_view',
])


class IMLSVocabularySettings(Interface):
    """Propertyshelf MLS settings for vocabularies.

    This describes records stored in the configuration registry and obtainable
    via plone.registry.
    """

    geographic_types_priority = schema.Text(
        description=MSG_PRIORITY_DESCRIPTION % POSSIBLE_GEOGRAPHIC_TYPES,
        required=False,
        title=_(u"'Geographic Types' priority list"),
    )

    listing_types_priority = schema.Text(
        description=MSG_PRIORITY_DESCRIPTION % POSSIBLE_LISTING_TYPES,
        required=False,
        title=_(u"'Listing Types' priority list"),
    )

    location_types_priority = schema.Text(
        description=MSG_PRIORITY_DESCRIPTION % POSSIBLE_LOCATION_TYPES,
        required=False,
        title=_(u"'Location Types' priority list"),
    )

    object_types_priority = schema.Text(
        description=MSG_PRIORITY_DESCRIPTION % POSSIBLE_OBJECT_TYPES,
        required=False,
        title=_(u"'Object Types' priority list"),
    )

    ownership_types_priority = schema.Text(
        description=MSG_PRIORITY_DESCRIPTION % POSSIBLE_OWNERSHIP_TYPES,
        required=False,
        title=_(u"'Ownership Types' priority list"),
    )

    view_types_priority = schema.Text(
        description=MSG_PRIORITY_DESCRIPTION % POSSIBLE_VIEW_TYPES,
        required=False,
        title=_(u"'View Types' priority list"),
    )
