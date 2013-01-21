# -*- coding: utf-8 -*-

import json
import unittest2 as unittest

from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from openmultimedia.api.interfaces import IVideoAPI

from openmultimedia.api.testing import INTEGRATION_TESTING
#from openmultimedia.api.testing import setupTestContent


class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pc = getToolByName(self.portal, 'portal_catalog')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.video_api = getUtility(IVideoAPI)

        self.test_url = ("http://multimedia.tlsur.net/api/clip/vallejo-"
                         "el-conflicto-debe-resolverse-con-los-"
                         "estudiantes/?detalle=completo")

    def test_get_json(self):
        base_url = 'http://localhost:15555'

        results = self.video_api.get_json(self.test_url)
        self.assertIs(type(results), dict)
        results = self.video_api.get_json("http://www.google.com")
        self.assertEqual(results, [])

        results = self.video_api.get_json("%s/video_api/get_json/good_response" % base_url)
        self.assertEqual(results, [])
        results = self.video_api.get_json("%s/video_api/get_json/not_found" % base_url)
        self.assertEqual(results, [])
        results = self.video_api.get_json("%s/video_api/get_json/internal_error" % base_url)
        self.assertEqual(results, [])
        results = self.video_api.get_json("%s/video_api/get_json/timeout" % base_url)
        self.assertEqual(results, [])
        results = self.video_api.get_json("%s/video_api/get_json/error_response" % base_url)
        self.assertEqual(results, [])

    def test_get_widgets(self):
        today = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                         'cmswidgets/videos.html?widget=mas_vistos'
                         '&amp;tiempo=dia'),
                 'title': u'Most seen today'}
        week = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                        'cmswidgets/videos.html?widget=mas_vistos'
                        '&amp;tiempo=semana'),
                'title': u'Most seen this week'}
        month = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                         'cmswidgets/videos.html?widget=mas_vistos'
                         '&amp;tiempo=mes'),
                 'title': u'Most seen this month'}
        year = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                        'cmswidgets/videos.html?widget=mas_vistos'
                        '&amp;tiempo=ano'),
                'title': u'Most seen this year'}

        results = self.video_api.get_videos_most_seen_widgets(['today'])

        self.assertIn(today, results)
        self.assertNotIn(week, results)
        self.assertNotIn(month, results)
        self.assertNotIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['today',
                                                               'week'])

        self.assertIn(today, results)
        self.assertIn(week, results)
        self.assertNotIn(month, results)
        self.assertNotIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['today',
                                                               'week',
                                                               'month'])

        self.assertIn(today, results)
        self.assertIn(week, results)
        self.assertIn(month, results)
        self.assertNotIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['today',
                                                               'week',
                                                               'month',
                                                               'year'])

        self.assertIn(today, results)
        self.assertIn(week, results)
        self.assertIn(month, results)
        self.assertIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['week',
                                                               'month',
                                                               'year'])

        self.assertNotIn(today, results)
        self.assertIn(week, results)
        self.assertIn(month, results)
        self.assertIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['month',
                                                               'year'])

        self.assertNotIn(today, results)
        self.assertNotIn(week, results)
        self.assertIn(month, results)
        self.assertIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['year'])

        self.assertNotIn(today, results)
        self.assertNotIn(week, results)
        self.assertNotIn(month, results)
        self.assertIn(year, results)

    def test_get_video_widget_url(self):
        results = self.video_api.get_video_widget_url(self.test_url)

        self.assertEqual(results, (u"http://multimedia.telesurtv.net/"
                                   "player/insertar.js?archivo=clips/"
                                   "telesur-video-2011-10-14-201605224901"
                                   ".mp4&amp;width=400"))

    def test_get_video_thumb(self):
        """
        get_video_thumb should return an url,
        an empty string indicates an error.
        """
        results = self.video_api.get_video_thumb(self.test_url)
        self.assertNotEqual(results, '')
        results = self.video_api.get_video_thumb(self.test_url,
                                                 thumb_size='medium')
        self.assertNotEqual(results, '')
        results = self.video_api.get_video_thumb(self.test_url,
                                                 thumb_size='large')
        self.assertNotEqual(results, '')

    def test_get_section_latest_videos_widget(self):

        url = ("http://multimedia.telesurtv.net/media/video/cmswidgets/videos"
               ".html?widget=ultimos_seccion&amp;seccion_plone=")

        categories_list = ['latinoamerica', 'vuelta-al-mundo', 'deportes',
                           'ciencia', 'cultura', 'salud', 'tecnologia']

        for i in categories_list:
            results = self.video_api.get_latest_from_section_video_widget(i)
            self.assertEqual(results, url + i)

    def test_get_basic_clip_list(self):

        results = self.video_api.get_basic_clip_list()
        self.assertEqual(results,
                         (u'http://multimedia.tlsur.net/api/clip/?'
                          'detalle=basico'))

        results = self.video_api.get_basic_clip_list(limit=10)
        self.assertEqual(results,
                         (u'http://multimedia.tlsur.net/api/clip/?'
                          'limit=10&detalle=basico'))

        results = self.video_api.get_basic_clip_list(offset=10, limit=10)
        self.assertEqual(results,
                         (u'http://multimedia.tlsur.net/api/clip/?'
                          'limit=10&detalle=basico&offset=10'))

    def test_get_section_latest_videos(self):

        categories_list = ['latinoamerica', 'vuelta-al-mundo', 'deportes',
                           'ciencia', 'cultura', 'salud', 'tecnologia']

        for i in categories_list:
            results = self.video_api.get_latest_videos_from_section(i)
            results = json.loads(results)
            self.assertEqual(len(results), 4)
            self.assertEqual(type(results), list)

    def test_get_most_seen_videos(self):
        results = self.video_api.get_videos_most_seen(['today'])
        results = json.loads(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)

        results = self.video_api.get_videos_most_seen(['today',
                                                       'week'])

        results = json.loads(results)

        self.assertEqual(len(results), 2)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)

        results = self.video_api.get_videos_most_seen(['today',
                                                       'week',
                                                       'month'])

        results = json.loads(results)

        self.assertEqual(len(results), 3)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)

        results = self.video_api.get_videos_most_seen(['today',
                                                       'week',
                                                       'month',
                                                       'year'])

        results = json.loads(results)

        self.assertEqual(len(results), 4)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)

        results = self.video_api.get_videos_most_seen(['week',
                                                       'month',
                                                       'year'])

        results = json.loads(results)

        self.assertEqual(len(results), 3)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)

        results = self.video_api.get_videos_most_seen(['month',
                                                       'year'])

        results = json.loads(results)

        self.assertEqual(len(results), 2)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)

        results = self.video_api.get_videos_most_seen(['year'])

        results = json.loads(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(type(results), list)
        for i in results:
            self.assertEqual(len(i['videos']), 5)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
