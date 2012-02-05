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
"""Article Provider."""

# zope imports
from Products.CMFCore.utils import getToolByName
from raptus.article.core.interfaces import IArticle
from zope.component import adapts
from zope.interface import implements


# local imports
from plone.mls.listing.article.interfaces import IListingLists


class ListingLists(object):
    """Provider for listings contained in an article."""
    implements(IListingLists)
    adapts(IArticle)

    def __init__(self, context):
        self.context = context

    def getListingLists(self, **kwargs):
        """Returns a list of listings (catalog brains)."""
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(
            portal_type='plone.mls.listing.listing',
            path={
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1,
            },
            sort_on='getObjPositionInParent', **kwargs)
