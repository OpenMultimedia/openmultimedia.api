# -*- coding: utf-8 -*-
import urllib2

from OFS.Image import Image

from five import grok

from zope.annotation.interfaces import IAnnotations

from zope.component import getMultiAdapter
from zope.component import getUtility

from zope.event import notify

from zope.interface import Interface

from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interfaces.link import IATLink

from Products.Archetypes.event import ObjectInitializedEvent

from openmultimedia.api.interfaces import IVideoAPI


class ManageVideoInContext(grok.View):
    grok.context(Interface)
    grok.name("manage-video-in-context")
    grok.require("zope2.View")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        titles = self.request.get('titles[]', [])
        urls = self.request.get('urls[]', [])
        types = self.request.get('media-types[]', [])
        if not isinstance(urls, list):
            urls = [urls]
        if not isinstance(titles, list):
            titles = [titles]
        if not isinstance(types, list):
            types = [types]
        media_brains = self.get_media()
        medias_urls = []
        for brain in media_brains:
            media_obj = brain.getObject()
            if media_obj.portal_type == 'openmultimedia.contenttypes.audio':
                medias_urls.append(media_obj.audio_url)
            else:
                medias_urls.append(media_obj.video_url)

        normalizer = getUtility(IIDNormalizer)
        for index, media in enumerate(medias_urls):
            if media not in urls:
                self.context.manage_delObjects(media_brains[index].id)
        if urls and titles and len(urls) == len(titles) and len(types) == len(urls):
            for index, url in enumerate(urls):
                url_s = url.strip()
                if url_s not in medias_urls:
                    title = titles[index].strip()
                    id = normalizer.normalize(title)
                    if id:
                        if id not in self.context:
                            if len(types) > index and types[index] == 'audio':
                                self.context.invokeFactory('openmultimedia.contenttypes.audio',
                                                           id, title=title, remote_url=url_s)
                            else:
                                self.context.invokeFactory('openmultimedia.contenttypes.video',
                                                           id, title=title, remote_url=url_s)
                        link = self.context[id]
                        notify(ObjectInitializedEvent(link))

    def get_videos(self):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=['Video'], path=path,
                         sort_on='getObjPositionInParent')
        return brains

    def get_audios(self):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=['Audio'], path=path,
                         sort_on='getObjPositionInParent')
        return brains

    def get_media(self):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=['Video', 'Audio'], path=path,
                         sort_on='getObjPositionInParent')

        return brains

    def render(self):
        return ""
