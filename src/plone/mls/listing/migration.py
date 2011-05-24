# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2011 Propertyshelf, LLC and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Migration steps for plone.mls.listing."""

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import getUtility

LISTING_TYPE = 'plone.mls.listing.listing'


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Update TinyMCE linkable types.
    * Update Kupu linkable types if available.
    """
    site = getUtility(IPloneSiteRoot)

    tinymce = getToolByName(site, 'portal_tinymce', None)
    if tinymce is not None:
        if LISTING_TYPE not in tinymce.linkable:
            tinymce.linkable += '\n' + LISTING_TYPE

    portal_types = getToolByName(site, 'portal_types')
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        linkable = list(kupu.getPortalTypesForResourceType('linkable'))
        if LISTING_TYPE not in linkable:
            # Kupu's resource list can accumulate old, no longer valid types.
            # It will throw an exception if we try to resave them.
            # So, let's clean the list.
            valid_types = dict([ (t.id, 1) for t in portal_types.listTypeInfo()])
            linkable = [pt for pt in linkable if pt in valid_types]

            linkable.append(LISTING_TYPE)
            kupu.updateResourceTypes(({
                'resource_type': 'linkable',
                'old_type': 'linkable',
                'portal_types': linkable,
            },))


def migrate_to_1002(context):
    """Migrate from 1001 to 1002.

    * Add plone.mls.listing.listing to Article's allowd types.
    * Add versioning behavior.
    * Enable versioning in portal types.
    """
    site = getUtility(IPloneSiteRoot)
    portal_types = getToolByName(site, 'portal_types')
    portal_repository = getToolByName(site, 'portal_repository')
    quickinstaller = getToolByName(site, 'portal_quickinstaller')

    # 1. Add plone.mls.featured.featured to Article's allowd types.
    if quickinstaller.isProductInstalled('raptus.article.core'):
        article = portal_types.get('Article', None)
        if article is None:
            return
        if not LISTING_TYPE in article.allowed_content_types:
            article.allowed_content_types += (LISTING_TYPE, )

    # 2. Add versioning behavior.
    try:
        import plone.app.versioningbehavior
    except ImportError:
        pass
    else:
        listing = portal_types.get(LISTING_TYPE, None)
        if listing is None:
            return
    
        versioning_behavior = 'plone.app.versioningbehavior.behaviors.IVersionable'
        if not versioning_behavior in listing.behaviors:
            listing.behaviors += (versioning_behavior, )

    # 3. Enable versioning in portal types.
    versionable_types = list(portal_repository.getVersionableContentTypes())
    if LISTING_TYPE not in versionable_types:
        # Use append() to make sure we don't overwrite any content types which
        # may already be under version control.
        versionable_types.append(LISTING_TYPE)
        # Add default versioning policies to the versioned type.
        for policy_id in DEFAULT_POLICIES:
            portal_repository.addPolicyForContentType(LISTING_TYPE, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)
