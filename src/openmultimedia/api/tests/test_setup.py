# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from openmultimedia.api.config import PROJECTNAME
from openmultimedia.api.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getattr(self.portal, 'portal_quickinstaller')

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IOpenmultimediaAPILayer' in layers,
                        'browser layer not installed')

    def test_javascript_registry(self):
        portal_javascripts = self.portal.portal_javascripts
        resources = portal_javascripts.getResourceIds()
        self.assertTrue('++resource++openmultimedia.api/addvideos.js' in
                                                                   resources)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('IOpenmultimediaAPILayer' in layers,
                         'browser layer not removed')

    def test_javascript_registry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        resources = portal_javascripts.getResourceIds()
        self.assertFalse('++resource++openmultimedia.api/addvideos.js' in
                                                                   resources)



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
