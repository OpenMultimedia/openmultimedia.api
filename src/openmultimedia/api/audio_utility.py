# -*- coding: utf-8 -*-
from zope.component import getUtility

from zope.interface import implements

from plone.registry.interfaces import IRegistry

from openmultimedia.api.interfaces import IAPISettings
from openmultimedia.api.interfaces import IVideoAPI
from openmultimedia.api.interfaces import IAudioAPI


class AudioAPI(object):
    """
    This utility will handle the communication between the multimedia system
    and the Plone site, in relation with the audio
    """

    implements(IAudioAPI)

    def get_audio_widget_url(self, url, width=400, json=None):
        video_api = getUtility(IVideoAPI)
        result = video_api.get_video_widget_url(url, width, json)
        if result:
            registry = getUtility(IRegistry)
            records = registry.forInterface(IAPISettings)
            audio_only = records.audio_only
            return "%s&amp;%s" % (result, audio_only)
