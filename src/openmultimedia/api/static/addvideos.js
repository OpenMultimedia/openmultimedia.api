
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

$(function() {
        $("#form-widgets-IAddableVideos-relatedVideos-contenttree-window #list-contents").change(
            function() {
                $("#form-widgets-search-videos-submit").trigger("click");
            }
        );
    if($("#relatedVideos").length) {
        $("#form-widgets-IAddableVideos-relatedVideos-contenttree-window").draggable();
		$( "#relatedVideos ul.from .navTreeItem").liveDraggable({ containment: ".relatedVideos",  scroll: false, helper: "clone"});
        $("#relatedVideos ul.recieve").droppable({
        			activeClass: "ui-state-default",
        			hoverClass: "ui-state-hover",
        			drop: function(event, ui) {
        			  var children = $(this).children();
        			  var i = 0;
        			  var exists = false;
        			  for(i=0; i<children.length; i++) {
                        if (ui.draggable.attr('uid') !== undefined ){
            			    if(ui.draggable.attr('uid') == $(children[i]).attr('uid')){
            			      exists = true;
            			    }
                        }
                        if ($("a",ui.draggable).length ){
            			    if($("a",ui.draggable).attr('href') == $("a",$(children[i])).attr('href')){
            			      exists = true;
            			    }
                        }
        			  }
        			  if(!exists) {
        			    var clon = ui.draggable.clone();
        			    var children = $("ul",clon);
        			    if(children.length) {
        			      children.remove();
        			    }
        			    clon.append("<div class='related-item-close'>X</div>");
        			    clon.appendTo( this );
        			  }
        			}
        		}).sortable();
    $("#relatedVideos ul.recieve li").append("<div class='related-item-close'>X</div>");
    $("#relatedVideos ul.recieve li a").live("click", function(e) {
      e.preventDefault();
      return false;
    });
    $(".related-item-close").live("click", function() {
        $(this).parent().remove();
    });
}

	$('#plone-contentmenu-factories #openmultimedia-api-multimedia').click(function(event) {
	    event.preventDefault();
	    $('.contenttreeWindow').showDialog();
	    firstLoad();
	});
});

if(jQuery) (function($){
    $.extend($.fn, {
        contentTreeAddVideos: function() {
            var data_url = [];
            var data_title = [];
            var data_type = [];
            $("#videos-loading-spinner-add").css("display", "block");
            $(".ui-droppable > li > a").each(function () {
                data_url.push($(this).attr('href'));
                data_title.push($(this).text());
                data_type.push($(this).attr("data-type"));
                removeVideoFromDroppable($(this));
            });
            jQuery.ajax({type: 'POST',
                url: '@@manage-video-in-context',
                async : false,
                data: {'titles':data_title,
                    'urls':data_url, 'media-types': data_type},
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
