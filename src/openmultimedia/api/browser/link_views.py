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
from Products.Archetypes.interfaces import IObjectInitializedEvent

from openmultimedia.api.interfaces import IVideoAPI


# XXX: do we still need this?
class LinkApi(grok.View):
    grok.context(IATLink)
    grok.name("link_api")
    grok.require("zope2.View")

    def get(self, element):
        annotations = IAnnotations(self.context)
        return annotations.get(element, None)

    def is_video(self):
        return self.get('archivo_url') and True or False

    def render(self):
        return self


class LinkPreviewSmallThumbnailView(grok.View):
    grok.context(IATLink)
    grok.name("small_thumbnail")
    grok.require("zope2.View")

    def render(self):
        link_api = getMultiAdapter((self.context, self.request),
                                       name="link_api")
        thumb = link_api.get('small_thumbnail')

        if thumb:
            return thumb.index_html(self.request, self.request.RESPONSE)
        else:
            return ''


class LinkPreviewMediumThumbnailView(grok.View):
    grok.context(IATLink)
    grok.name("medium_thumbnail")
    grok.require("zope2.View")

    def render(self):
        link_api = getMultiAdapter((self.context, self.request),
                                       name="link_api")
        thumb = link_api.get('medium_thumbnail')

        if thumb:
            return thumb.index_html(self.request, self.request.RESPONSE)
        else:
            return ''


class LinkPreviewLargeThumbnailView(grok.View):
    grok.context(IATLink)
    grok.name("large_thumbnail")
    grok.require("zope2.View")

    def render(self):
        link_api = getMultiAdapter((self.context, self.request),
                                       name="link_api")
        thumb = link_api.get('large_thumbnail')

        if thumb:
            return thumb.index_html(self.request, self.request.RESPONSE)
        else:
            return ''


class UpdateLinkView(grok.View):
    grok.context(IATLink)
    grok.name("update-link")
    grok.require("cmf.ModifyPortalContent")

    def __call__(self):
        request = self.request
        link_control = getMultiAdapter((self.context, request),
                                       name="link-control")
        link_control.update_local_data(self.context)
        view_url = self.context.absolute_url()
        self.request.response.redirect(view_url)

    def render(self):
        return "update-link"


class LinkControl(grok.View):
    grok.context(IATLink)
    grok.name("link-control")
    grok.require("cmf.ModifyPortalContent")

    def update_local_data(self, element):
        annotations = IAnnotations(element)
        video_api = getUtility(IVideoAPI)
        url = element.remoteUrl
        json = video_api.get_json(url)

        if json:
            thumb_small = video_api.get_video_thumb(url, 'small', json)
            thumb_med = video_api.get_video_thumb(url, 'medium', json)
            thumb_large = video_api.get_video_thumb(url, 'large', json)

            archivo_url = json.get('archivo_url', None)
            audio_url = json.get('audio_url', None)
            titulo = json.get('titulo', None)
            descripcion = json.get('descripcion', None)
            slug = json.get('slug', None)

            if thumb_small:
                data = urllib2.urlopen(thumb_small)
                img = Image('small_thumbnail', 'Small thumbnail', data.read())
                annotations['small_thumbnail'] = img
            else:
                try:
                    del(annotations['small_thumbnail'])
                except KeyError:
                    pass

            if thumb_med:
                data = urllib2.urlopen(thumb_med)
                img = Image('medium_thumbnail',
                            'Medium thumbnail',
                            data.read())
                annotations['medium_thumbnail'] = img
            else:
                try:
                    del(annotations['medium_thumbnail'])
                except KeyError:
                    pass

            if thumb_large:
                data = urllib2.urlopen(thumb_large)
                img = Image('large_thumbnail', 'Large thumbnail', data.read())
                annotations['large_thumbnail'] = img
            else:
                try:
                    del(annotations['large_thumbnail'])
                except KeyError:
                    pass

            if archivo_url:
                annotations['archivo_url'] = archivo_url
            else:
                try:
                    del(annotations['archivo_url'])
                except KeyError:
                    pass

            if audio_url:
                annotations['audio_url'] = audio_url
            else:
                try:
                    del(annotations['audio_url'])
                except KeyError:
                    pass

            if titulo:
                annotations['titulo'] = titulo
                element.setTitle(titulo)
            else:
                try:
                    del(annotations['titulo'])
                except KeyError:
                    pass

            if descripcion:
                annotations['descripcion'] = descripcion
                element.setDescription(descripcion)
            else:
                try:
                    del(annotations['descripcion'])
                except KeyError:
                    pass

            if slug:
                annotations['slug'] = slug
            else:
                try:
                    del(annotations['slug'])
                except KeyError:
                    pass

    def render(self):
        return self


class AddVideoToContext(grok.View):
    grok.context(Interface)
    grok.name("add-video-to-context")
    grok.require("zope2.View")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, title, url):
        title = title.strip()
        url = url.strip()
        normalizer = getUtility(IIDNormalizer)
        id = normalizer.normalize(title)
        if id not in self.context:
            self.context.invokeFactory('openmultimedia.contenttypes.video', id, title=title, remote_url=url)
        link = self.context[id]
        notify(ObjectInitializedEvent(link))

    def render(self):
        return u"add-video-to-context"


class ManageVideoInContext(grok.View):
    grok.context(Interface)
    grok.name("manage-video-in-context")
    grok.require("zope2.View")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        titles = self.request.get('titles[]', None)
        urls = self.request.get('urls[]', None)
        videos_brain = self.get_videos()
        videos = [video.getObject().video_url for video in self.get_videos()]
        normalizer = getUtility(IIDNormalizer)
        for index, video in enumerate(videos):
            if video not in urls:
                video_id = videos_brain[index].id
                self.context.manage_delObjects(videos_brain[index].id)
        if urls:
            for index, url in enumerate(urls):
                url_s = url.strip()
                if url_s not in videos:
                    title = titles[index].strip()
                    id = normalizer.normalize(title)
                    if id:
                        if id not in self.context:
                            self.context.invokeFactory('openmultimedia.contenttypes.video', id, title=title, remote_url=url_s)
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

    def render(self):
        return ""

        # title = title.strip()
        #         url = url.strip()
        #         normalizer = getUtility(IIDNormalizer)
        #         id = normalizer.normalize(title)
        #         if id not in self.context:
        #             self.context.invokeFactory('openmultimedia.contenttypes.video', id, title=title, remote_url=url)
        #         link = self.context[id]
        #         notify(ObjectInitializedEvent(link))


# XXX: unregister subscriber because is causing issues with standard links
#@grok.subscribe(IATLink, IObjectInitializedEvent)
def update_local_data(obj, event):
    request = obj.REQUEST
    link_control = getMultiAdapter((obj, request), name="link-control")
    link_control.update_local_data(obj)
