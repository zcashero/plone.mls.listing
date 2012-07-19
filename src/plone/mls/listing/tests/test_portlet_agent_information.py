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
"""Test plone.mls.listing Agent Information portlet."""

# python imports
import unittest2 as unittest

# zope imports
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import TEST_USER_ID, setRoles
from plone.portlets import interfaces
from zope.component import getMultiAdapter, getUtility

# local imports
from plone.mls.listing.portlets import agent_information
from plone.mls.listing.testing import PLONE_MLS_LISTING_INTEGRATION_TESTING


class TestAgentInformationPortlet(unittest.TestCase):
    """Test Case for the Agent Information portlet."""

    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))
        self.portlet = getUtility(interfaces.IPortletType,
                                  name='portlets.AgentInformation')

    def test_portlet_type_registered(self):
        self.assertEqual(self.portlet.addview, 'portlets.AgentInformation')

    def test_interfaces(self):
        portlet = agent_information.Assignment()
        self.assertTrue(interfaces.IPortletAssignment.providedBy(portlet))
        self.assertTrue(
            interfaces.IPortletDataProvider.providedBy(portlet))

    def test_invoke_add_view(self):
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for item in mapping.keys():
            del mapping[item]
        addview = mapping.restrictedTraverse('+/' + self.portlet.addview)
        addview.createAndAdd(data={})
        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0],
                                   agent_information.Assignment))

    def test_invoke_edit_view(self):
        request = self.layer['request']
        mapping = PortletAssignmentMapping()
        mapping['foo'] = agent_information.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertIsInstance(editview, agent_information.EditForm)

    def test_renderer(self):
        request = self.layer['request']
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(interfaces.IPortletManager,
            name='plone.rightcolumn', context=self.portal)
        assignment = agent_information.Assignment()
        renderer = getMultiAdapter(
            (self.portal, request, view, manager, assignment),
            interfaces.IPortletRenderer)
        self.assertIsInstance(renderer, agent_information.Renderer)


class TestRenderer(unittest.TestCase):
    """Test Case for the Agent Information portlet renderer."""

    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))
