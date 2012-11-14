# -*- coding: utf-8 -*-

from five import grok

import z3c.form.interfaces

from zope.interface import Interface

from openmultimedia.api.behavior import IAddableVideos
from openmultimedia.api.widgets.video import AddVideosWidget


class FilterVideos(grok.View):
    grok.context(Interface)
    grok.name("filter-related-videos")
    grok.require("zope2.View")

    def __call__(self, query=None, content_type=None, offset=0):
        field = IAddableVideos.get('relatedVideos')
        request = self.request

        widget = z3c.form.interfaces.IFieldWidget(field,
                                                  AddVideosWidget(request))

        # XXX: REDO
        widget.context = self.context
        result = widget.render_tree(query=query, content_type=content_type, limit=10, offset=int(offset))

        return result.strip()

    def render(self):
        return "filter-related-videos"
