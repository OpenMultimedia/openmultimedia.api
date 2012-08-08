
function addVideoToContainer(video){
    var title = video.text();
    var url = video.attr('href');
    if ( title != "" && url !== undefined ){
        jQuery.ajax({type: 'POST',
                        url: '@@add-video-to-context',
                        async : false,
                        data: {'title':title,
                               'url':url},
                        success: function(results){
                            // XXX: Do we need to do something with the results ?
                                }
                    });
    }
}

if(jQuery) (function($){
    $.extend($.fn, {
        contentTreeAddVideos: function() {
            var data_url = []
            var data_title = []
            $("#videos-loading-spinner-add").css("display", "block");
            $(".ui-droppable > li > a").each(function () {
                data_url.push($(this).attr('href'));
                data_title.push($(this).text());
                //addVideoToContainer($(this));
                removeVideoFromDroppable($(this));
            });
            jQuery.ajax({type: 'POST',
                url: '@@manage-video-in-context',
                async : false,
                data: {'titles':data_title,
                    'urls':data_url},
                success: function(results){
                    $("#videos-loading-spinner-add").css("display", "none");
                // XXX: Do we need to do something with the results ?
                }
            });
            $(this).contentTreeCancel();
            window.location.reload();
        }
    });

})(jQuery);
