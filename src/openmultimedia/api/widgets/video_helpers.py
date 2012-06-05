# -*- coding: utf-8 -*-

import z3c.form.interfaces

from Products.Five.browser import BrowserView

from openmultimedia.api.behavior import IAddableVideos
from openmultimedia.api.widgets.video import AddVideosWidget

class FilterVideos(BrowserView):

    def __call__(self, query=None, offset=0):
        field = IAddableVideos.get('relatedVideos')
        request = self.request

        widget = z3c.form.interfaces.IFieldWidget(field,
                                                  AddVideosWidget(request))

        # XXX: REDO
        widget.context = self.context
        result = widget.render_tree(query=query, limit=10, offset=int(offset))

        return result.strip()