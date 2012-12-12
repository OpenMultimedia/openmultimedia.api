# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from openmultimedia.api.interfaces import IAudioAPI

from openmultimedia.api.testing import INTEGRATION_TESTING
#from openmultimedia.api.testing import setupTestContent


class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pc = getToolByName(self.portal, 'portal_catalog')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.audio_api = getUtility(IAudioAPI)

        self.test_url = ("http://multimedia.tlsur.net/api/clip/vallejo-"
                         "el-conflicto-debe-resolverse-con-los-"
                         "estudiantes/?detalle=completo")

    def test_get_audio_widget_url(self):
        returned_url = (u'http://multimedia.telesurtv.net/player/insertar.js'
                        '?archivo=clips/telesur-video-2011-10-14-'
                        '201605224901.mp4&amp;width=400&amp;solo_audio=true')
        results = self.audio_api.get_audio_widget_url(self.test_url)
        self.assertEquals(results, returned_url)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
