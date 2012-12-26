# -*- coding: utf-8 -*-

from zope.component import adapts

from zope.interface import implements
from zope.interface import alsoProvides

from z3c.form.interfaces import IDisplayForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

from plone.autoform.interfaces import IFormFieldProvider

from plone.dexterity.interfaces import IDexterityContainer
from plone.directives import form

from plone.formwidget.contenttree import ObjPathSourceBinder

from openmultimedia.api.widgets.video import AddVideosFieldWidget
from openmultimedia.api import _


class IAddableVideos(form.Schema):
    """
    """

    form.omitted('relatedVideos')
    form.no_omit(IDisplayForm, 'relatedVideos')
    form.widget(relatedVideos=AddVideosFieldWidget)
    form.read_permission(relatedVideos='cmf.ModifyPortalContent')
    relatedVideos = RelationList(
        title=_(u'Related videos'),
        default=[],
        value_type=RelationChoice(title=_(u'Related videos'),
                                  source=ObjPathSourceBinder()),
        required=False,
    )

alsoProvides(IAddableVideos, IFormFieldProvider)


class AddableVideos(object):
    """
    """
    implements(IAddableVideos)
    # Only for containers
    adapts(IDexterityContainer)

    def __init__(self, context):
        self.context = context
