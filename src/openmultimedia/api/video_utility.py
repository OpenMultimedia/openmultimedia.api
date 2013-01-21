# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import re
import logging

from socket import timeout

from zope.component import getUtility

from zope.interface import implements

from plone.registry.interfaces import IRegistry

from openmultimedia.api.config import PROJECTNAME
from openmultimedia.api.interfaces import IAPISettings
from openmultimedia.api.interfaces import IVideoAPI
from openmultimedia.api import _


logger = logging.getLogger(PROJECTNAME)


class VideoAPI(object):
    """
    This utility will handle the communication between the multimedia system
    and the Plone site, in relation with the videos
    """

    implements(IVideoAPI)

    def get_json(self, url):
        result = []
        if url:
            try:
                data = urllib2.urlopen(url, timeout=6)
            except urllib2.HTTPError:
                logger.info("An error ocurred when trying to access %s" % url)
                data = None
            except (urllib2.URLError, timeout):
                logger.info("Timeout when trying to access %s" % url)
                data = None

            if data:
                try:
                    result = json.load(data)
                except ValueError:
                    result = []

                if result and 'Error' in result:
                    result = []

        return result

    def query(self, **kwargs):
        if kwargs:
            registry = getUtility(IRegistry)
            records = registry.forInterface(IAPISettings)
            url_base = self.get_multimedia_url()
            video_api = records.video_api

            query_url = "%s%s%s" % (url_base,
                                    video_api,
                                    urllib.urlencode(kwargs))

            return self.get_json(query_url)

        raise ValueError("No arguments supplied")

    def get_multimedia_url(self):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        url_base = records.url_base

        return url_base

    def get_video_widget_url(self, url, width=400, json=None):
        if json:
            video_info = json
        else:
            video_info = self.get_json(url)

        widget_width = u"&amp;width=%s" % width
        if video_info:
            if 'archivo_url' in video_info:
                registry = getUtility(IRegistry)
                records = registry.forInterface(IAPISettings)
                video_regex_string = records.video_regex_string
                video_widget_url_base = records.video_widget_url_base
                video_regex = re.compile(video_regex_string)

                video_url = video_info['archivo_url']
                match = video_regex.search(video_url)
                if match:
                    clip_url = match.groups()[0]
                    return video_widget_url_base + clip_url + widget_width

    def get_videos_most_seen_widgets(self, moments):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)
        most_seen_widget = records.most_seen_widget
        time_filter_day = records.time_filter_day
        time_filter_week = records.time_filter_week
        time_filter_month = records.time_filter_month
        time_filter_year = records.time_filter_year

        widgets = []

        #XXX: This should be done with urlencode
        if 'today' in moments:
            widget = {'title': _(u"Most seen today"),
                      'url': "%s&amp;%s" % (most_seen_widget,
                                            time_filter_day),
                      }
            widgets.append(widget)

        #XXX: This should be done with urlencode
        if 'week' in moments:
            widget = {'title': _(u"Most seen this week"),
                      'url': "%s&amp;%s" % (most_seen_widget,
                                            time_filter_week),
                      }
            widgets.append(widget)

        #XXX: This should be done with urlencode
        if 'month' in moments:
            widget = {'title': _(u"Most seen this month"),
                      'url': "%s&amp;%s" % (most_seen_widget,
                                            time_filter_month),
                      }
            widgets.append(widget)

        #XXX: This should be done with urlencode
        if 'year' in moments:
            widget = {'title': _(u"Most seen this year"),
                      'url': "%s&amp;%s" % (most_seen_widget,
                                            time_filter_year),
                      }
            widgets.append(widget)

        return widgets

    def get_video_thumb(self, url, thumb_size='small', json=None):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        if json:
            json_data = json
        else:
            json_data = self.get_json(url)

        thumb_url = ''

        if thumb_size == 'small':
            thumb = records.video_thumbnail_small
        if thumb_size == 'medium':
            thumb = records.video_thumbnail_medium
        if thumb_size == 'large':
            thumb = records.video_thumbnail_large

        if json_data:
            if thumb in json_data:
                thumb_url = json_data[thumb]
        return thumb_url

    def get_latest_from_section_video_widget(self, section):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        # XXX: Get these into the IAPISettings interface, instead of
        #      hard-coding them here...
        categories_list = ['latinoamerica', 'vuelta-al-mundo', 'deportes',
                           'ciencia', 'cultura', 'salud', 'tecnologia']

        url = ''
        if section in categories_list:
            latest_from_section_widget = records.latest_from_section_widget
            url = "%s&amp;seccion_plone=%s" % (latest_from_section_widget,
                                               section)
        return url

    def get_basic_clip_list(self, offset=None, limit=None):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        url_base = self.get_multimedia_url()
        video_api = records.video_api

        offset_param = records.offset
        limit_param = records.limit
        details_param = records.details

        base_url = "%s%s" % (url_base, video_api)

        params = {details_param: 'basico'}

        if offset:
            params[offset_param] = offset

        if limit:
            params[limit_param] = limit

        params = urllib.urlencode(params)

        base_url += params

        return base_url

    def get_news_clip_list(self, offset=None, limit=None):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        url_base = records.url_base
        video_api = records.video_api

        offset_param = records.offset
        limit_param = records.limit
        details_param = records.details

        base_url = "%s%s" % (url_base, video_api)

        params = {details_param: 'basico', 'tipo': 'noticia'}

        if offset:
            params[offset_param] = offset

        if limit:
            params[limit_param] = limit

        params = urllib.urlencode(params)

        base_url += params

        return base_url

    def get_section_tag_clip_list(self, section=None, tag=None, offset=None, limit=None):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        url_base = records.url_base
        video_api = records.video_api

        offset_param = records.offset
        limit_param = records.limit
        details_param = records.details
        video_category = records.video_category
        video_region = records.video_region

        base_url = "%s%s" % (url_base, video_api)

        params = {details_param: 'completo', }

        if offset:
            params[offset_param] = offset

        if limit:
            params[limit_param] = limit

        if tag:
            params['tag'] = tag

        # Mimic the cmswidgets/controllers/ultimos_seccion_controller.js
        # functionality
        if section:
            if section == 'latinoamerica':
                params[video_region] = 'america-latina'
            elif section == 'vuelta-al-mundo':
                params[video_region] = 'excepto__america-latina'
            elif section == 'salud' or section == 'tecnologia':
                params[video_category] = 'ciencia'
            elif (section == 'deportes' or
                  section == 'ciencia' or
                  section == 'cultura', section == 'nacionales'):
                params[video_category] = section

        params = urllib.urlencode(params)

        base_url += params

        return base_url

    def get_latest_videos_from_section(self, section, limit=4):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        url_base = self.get_multimedia_url()
        video_api = records.video_api

        base_url = "%s%s" % (url_base, video_api)

        limit_param = records.limit
        details_param = records.details

        video_type = records.video_type
        video_region = records.video_region
        video_category = records.video_category

        # Ask for news, with basic set of results, and limiting results to 4
        params = {limit_param: limit,
                  details_param: 'basico',
                  video_type: 'noticia'}

        # Mimic the cmswidgets/controllers/ultimos_seccion_controller.js
        # functionality
        if section == 'latinoamerica':
            params[video_region] = 'america-latina'
        elif section == 'vuelta-al-mundo':
            params[video_region] = 'excepto__america-latina'
        elif section == 'salud' or section == 'tecnologia':
            params[video_category] = 'ciencia'
        elif (section == 'deportes' or
              section == 'ciencia' or
              section == 'cultura'):
            params[video_category] = section

        params = urllib.urlencode(params)

        base_url += params

        result = urllib.urlopen(base_url).read()

        return result

    def get_videos_most_seen(self, moments, limit=5):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)

        url_base = self.get_multimedia_url()
        video_api = records.video_api

        base_url = "%s%s" % (url_base, video_api)

        limit_param = records.limit
        details_param = records.details
        video_order = records.video_order

        params = {limit_param: limit,
                  details_param: 'basico',
                  video_order: 'popularidad'}

        params = urllib.urlencode(params)
        base_url += params

        widgets = []

        if 'today' in moments:
            result = urllib.urlopen(base_url).read()
            result = json.loads(result)

            widget = {'title': _(u"Most seen today"),
                      'videos': result,
                      }
            widgets.append(widget)

        if 'week' in moments:
            result = urllib.urlopen(base_url).read()
            result = json.loads(result)

            widget = {'title': _(u"Most seen this week"),
                      'videos': result,
                      }
            widgets.append(widget)

        if 'month' in moments:
            result = urllib.urlopen(base_url).read()
            result = json.loads(result)

            widget = {'title': _(u"Most seen this month"),
                      'videos': result,
                      }
            widgets.append(widget)

        if 'year' in moments:
            result = urllib.urlopen(base_url).read()
            result = json.loads(result)

            widget = {'title': _(u"Most seen this year"),
                      'videos': result,
                      }
            widgets.append(widget)

        return json.dumps(widgets)

    def get_widgets(self, widgets=True):
        if widgets:
            result = self.get_videos_most_seen_widgets(
                ['today', 'week', 'month'])
        else:
            result = self.get_videos_most_seen(['today', 'week', 'month'])

        return result

    def get_channels(self):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)
        url_base = records.url_base
        return self.get_json(url_base + "canal/")

    def get_content_types(self):
        registry = getUtility(IRegistry)
        records = registry.forInterface(IAPISettings)
        url_base = records.url_base
        return self.get_json(url_base + "tipo_contenido/")
