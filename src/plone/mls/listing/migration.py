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
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from plone.browserlayer import utils as layerutils
from zope.component import getUtility

# local imports
from plone.mls.listing.browser.interfaces import IListingSpecific


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

    try:
        from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
        # we're on plone < 4.1, configure versionable types manually
        setVersionedTypes(context)
    except ImportError:
        # repositorytool.xml will be used
        pass


def setVersionedTypes(context):
    # 3. Enable versioning in portal types.
    site = getUtility(IPloneSiteRoot)
    portal_repository = getToolByName(site, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    if LISTING_TYPE not in versionable_types:
        # Use append() to make sure we don't overwrite any content types which
        # may already be under version control.
        versionable_types.append(LISTING_TYPE)
        # Add default versioning policies to the versioned type.
        for policy_id in DEFAULT_POLICIES:
            portal_repository.addPolicyForContentType(LISTING_TYPE, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)


def migrate_to_1003(context):
    """Migrate from 1002 to 1003.

    * Add plone.mls.listing browser layer.
    * Register custom stylesheet.
    """
    site = getUtility(IPloneSiteRoot)

    if not IListingSpecific in layerutils.registered_layers():
        layerutils.register_layer(IListingSpecific, name='plone.mls.listing')

    portal_css = getToolByName(site, 'portal_css')
    portal_css.registerStylesheet('++resource++plone.mls.listing.stylesheets/main.css', media='screen')


def migrate_to_1004(context):
    """Migrate from 1003 to 1004.

    * Set 'Link using UIDs' for TinyMCE to false.
    """
    site = getUtility(IPloneSiteRoot)

    tinymce = getToolByName(site, 'portal_tinymce', None)
    if tinymce is not None:
        tinymce.link_using_uids = False
