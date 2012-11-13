# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.i18n import translate

import z3c.form.interfaces
import z3c.form.widget

from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from plone.app.layout.navigation.interfaces import INavtreeStrategy

from collective.z3cform.widgets.multicontent_search_widget \
    import MultiContentSearchWidget as BaseWidget

from openmultimedia.api.interfaces import IVideoAPI


class AddVideosWidget(BaseWidget):
    display_template = ViewPageTemplateFile('templates/add_videos_widget.pt')
    recurse_template = ViewPageTemplateFile('templates/recurse_videos_widget.pt')
    selected_template = ViewPageTemplateFile('templates/related_search.pt')
    list_channels_template = ViewPageTemplateFile('templates/list_channels.pt')

    def list_channels(self):
        video_api = getUtility(IVideoAPI)
        channel_json = video_api.get_channels()
        return self.list_channels_template(data=channel_json)

    def render_tree(self, query=None, channel=None, limit=10, offset=0):
        video_api = getUtility(IVideoAPI)

        data = []

        url = video_api.get_basic_clip_list(offset, limit)

        if query:
            url = "%s&texto=%s" % (url, query)
        if channel and channel != 'all':
            url = "%s&canal=%s" % (url, channel)

        json = video_api.get_json(url)
        for entry in json:
            if entry['api_url']:
                # This check shouldn't be needed since all results should have
                # videos... but, just in case...

                tmp = {'video_url': entry['api_url'],
                        'selectable': True,
                        'title': entry['titulo'],
                        'description': entry['descripcion'],
                        'date': DateTime(entry['fecha']).Date(),
                        'type': 'video'}
                if 'thumbnail_mediano' in entry.keys():
                    tmp['video_thumb'] = entry['thumbnail_mediano']
                if 'canal' in entry.keys():
                    canal_data = entry['canal']
                    data_type = canal_data['tipo']
                    if data_type != 'video':
                        tmp['type'] = 'audio'
                data.append(tmp)

        return self.recurse_template(children=data, level=1, offset=offset + limit)

    def js_extra(self):
        form_url = self.request.getURL()
        url = "%s/++widget++%s/@@contenttree-fetch" % (form_url, self.name)

        return """\

                $('#%(id)s-widgets-query').each(function() {
                    if($(this).siblings('input.searchButton').length > 0) { return; }
                    $(document.createElement('input'))
                        .attr({
                            'type': 'button',
                            'value': '%(button_val)s'
                        })
                        .addClass('searchButton')
                        .click( function () {
                            var parent = $(this).parents("*[id$='-autocomplete']")
                            var window = parent.siblings("*[id$='-contenttree-window']")
                            window.showDialog();
                            firstLoad();
                        }).insertAfter($(this));
                });
                $('#%(id)s-contenttree-window').find('.contentTreeAddVideos').unbind('click').click(function () {
                    $(this).contentTreeAddVideos();
                });
                $('#%(id)s-contenttree-window').find('.contentTreeCancel').unbind('click').click(function () {
                    $(this).contentTreeCancel();
                });
                if ($('#%(id)s-widgets-query')[0] !== undefined){
                    $('#%(id)s-widgets-query').after(" ");
                }
                $('#%(id)s-contenttree').contentTree(
                    {
                        script: '%(url)s',
                        folderEvent: '%(folderEvent)s',
                        selectEvent: '%(selectEvent)s',
                        expandSpeed: %(expandSpeed)d,
                        collapseSpeed: %(collapseSpeed)s,
                        multiFolder: %(multiFolder)s,
                        multiSelect: %(multiSelect)s,
                    },
                    function(event, selected, data, title) {
                        // alert(event + ', ' + selected + ', ' + data + ', ' + title);
                    }
                );
        """ % dict(url=url,
                   id=self.name.replace('.', '-'),
                   folderEvent=self.folderEvent,
                   selectEvent=self.selectEvent,
                   expandSpeed=self.expandSpeed,
                   collapseSpeed=self.collapseSpeed,
                   multiFolder=str(self.multiFolder).lower(),
                   multiSelect=str(self.multi_select).lower(),
                   name=self.name,
                   klass=self.klass,
                   title=self.title,
                   button_val=translate(
                       u'heading_contenttree_browse',
                       default=u'Browse for items',
                       domain='collective.formwidget.relationfield',
                       context=self.request))


    def filter_js(self):
        form_url = self.request.getURL()
        url = "%s/@@filter-related-videos" % self.context.absolute_url()

        return """\
        function removeVideoFromDroppable( $item ) {
            var $dropping = jq('#content-droppable');
            var $listing = jq('.contenttreeWidget .navTree');
            var $item_href = $item.find('a.ui-widget-content').attr('href');
            var $listing_item = $('.contenttreeWidget a@[href='+$item_href+']').parent();
            $listing_item.removeClass('navTreeCurrentItem');
            $listing_item.addClass("draggable");
            $item.remove();
        }

        function unbindClickEvent() {

            $('ul#content-droppable').unbind('click').click(function(event) {
                var $item = $(this);
                var $target = $(event.target);
                var $parent = $($target).parent();

                if ( $target.is("a.ui-icon-trash") ) {
                    removeVideoFromDroppable($parent);
                    return false
                    }
                if ( $target.is("a.ui-widget-content") ) {
                    return false
                    }
            });

            $('ul#related-content-videos > li > a').unbind('click').click(function(event) {
                return false

            });

        }

        function showLoadSpinner() {
        $("#videos-loading-spinner").css("display", "inline");
        }

        function hideLoadSpinner() {
        $("#videos-loading-spinner").css("display", "none");
        }

        function infiniteScrollVideo() {
            var opts = {context:'#related-content-videos', offset: '%(perc)s'};
            var $footer = $("#related-content-videos #show-more-results");
            $footer.waypoint(function(event, direction) {
            $footer.waypoint('remove');
            if(direction == 'down') {
                $("#show-more-results a").trigger("click");
            }
            }, opts);
        }

        function afterLoad() {
        unbindClickEvent();
        hideLoadSpinner();
        infiniteScrollVideo();
        }

        function filterVideos() {
        $("#related-content-videos").empty();
        showLoadSpinner();
        var query = document.getElementById('form-widgets-search-videos').value;
        var channel = $("#list-channels").val();
        $("ul#related-content-videos").load('%(url)s',{'query':query, 'channel': channel}, afterLoad);
        }

        function firstLoad(){
        showLoadSpinner();
        $("ul#related-content-videos").load('%(url)s',{}, afterLoad);
        }

        function showMoreSpinner() {
        $("#videos-more-spinner").css("display", "inline");
        }

        function hideMoreSpinner() {
        $("#videos-more-spinner").css("display", "none");
        }

        function appendMoreVideos(offset) {
            $("#show-more-results").remove();
            showMoreSpinner();
            var query = document.getElementById('form-widgets-search-videos').value;
            jQuery.ajax({type: 'POST',
                        url: '@@filter-related-videos',
                        async : true,
                        data: {'query':query,
                                'offset':offset},
                        success: function(results){
                                hideMoreSpinner();
                                $("ul#related-content-videos").append(results);
                                unbindClickEvent();
                                infiniteScrollVideo();
                                }
                            });
        }

        """ % dict(url=url, perc="100%")

    def render_selected(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                         name=u'plone_portal_state')
        portal = portal_state.portal()
        strategy = getMultiAdapter((portal, self), INavtreeStrategy)

        items = []

        medias = self.get_media()
        for brain in medias:
            media = brain.getObject()
            if media.portal_type == 'openmultimedia.contenttypes.audio':
                media_type = 'audio'
                media_url = media.audio_url
            else:
                media_type = 'video'
                media_url = media.video_url

            tmp = {'item': brain,
                'video_url': media_url,
                'type': media_type,
                'date': media.created().strftime("%d/%m/%Y")}
            if hasattr(media, 'image') and media.image:
                tmp['video_thumb'] = media.image.filename
            items.append(strategy.decoratorFactory(tmp))

        return self.selected_template(children=items, level=1)

    def get_videos(self):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=['Video'], path=path,
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


@implementer(z3c.form.interfaces.IFieldWidget)
def AddVideosFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, AddVideosWidget(request))
