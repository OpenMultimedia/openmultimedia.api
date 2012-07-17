# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer

import z3c.form.interfaces
import z3c.form.widget

from collective.z3cform.widgets.multicontent_search_widget \
    import MultiContentSearchWidget as BaseWidget

from zope.i18n import translate
from DateTime import DateTime

from openmultimedia.api.interfaces import IVideoAPI


class AddVideosWidget(BaseWidget):
    display_template = ViewPageTemplateFile('templates/add_videos_widget.pt')
    recurse_template = ViewPageTemplateFile('templates/recurse_videos_widget.pt')


    def render_tree(self, query=None, limit=10, offset=0):
        video_api = getUtility(IVideoAPI)

        data = []

        url = video_api.get_basic_clip_list(offset, limit)

        if query:
            url = "%s&texto=%s" % (url, query)

        json = video_api.get_json(url)

        for entry in json:
            if entry['api_url']:
                # This check shouldn't be needed since all results should have
                # videos... but, just in case...
                data.append(
                        {
                            'video_url': entry['api_url'],
                            'video_thumb': entry['thumbnail_mediano'],
                            'selectable': True,
                            'title': entry['titulo'],
                            'description': entry['descripcion'],
                            'date': DateTime(entry['fecha']).Date(),
                        }
                    )

        return self.recurse_template(children=data, level=1, offset=offset+limit)

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

        function afterLoad() {
        unbindClickEvent();
        hideLoadSpinner();
        }

        function filterVideos(){
        showLoadSpinner();
        var query = document.getElementById('form-widgets-search-videos').value;
        $("ul#related-content-videos").load('%(url)s',{'query':query}, afterLoad);
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
                                }
                            });
        }

        """ % dict(url=url)


@implementer(z3c.form.interfaces.IFieldWidget)
def AddVideosFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, AddVideosWidget(request))
