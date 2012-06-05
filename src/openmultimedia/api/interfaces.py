# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer

from openmultimedia.api import _


class IOpenmultimediaAPILayer(IDefaultPloneLayer):
    """ Default browser layer for openmultimedia.api """


class IAudioAPI(Interface):
    """
    Interface to be implemented by the audio utility
    """

    def get_audio_widget_url(url, width, json):
        """
        This method will get the Javascript used to embed the audio player
        http://[url]insertar.js?archivo=[archivo]&amp;width=[width]&solo_audio=true
        """

class IVideoAPI(Interface):
    """
    Interface to be implemented by the video utility
    """

    def get_json(url):
        """
        This method will return a JSON with the results from the given URL.
        If the result cannot be parsed as a JSON or if an error is returned,
        then we'll return None
        """

    def query(kwargs):
        """
        Allows to query the remote system. Raises an exception if no
        attributes are passed, then an exception is raised
        """

    def get_video_widget_url(url, width, json):
        """
        Method to obtain the Javascript used to embed the video player.
        http://[url]insertar.js?archivo=[archivo]&amp;width=[width]
        """

    def get_videos_most_seen_widgets(moments):
        """
        This method will return a list with most seen videos for each moment
        listed in the "moments" param.
        Valid values: "today", "week", "month", "year"
        e.g: get_videos_most_seen_widgets(['today','month']) will return both
        widgets
        """

    def get_widgets():
        """
        XXX: This remains here as backwards compatibility
        """

    def get_video_thumb(url, thumb_size, json):
        """
        A method to return the video thumbnail according to the requested
        size.
        Allowed sizes: 'small', 'medium', 'large'
        """

    def get_latest_from_section_video_widget(section):
        """
        Return a URL with the latest from section video widget
        """

    def get_basic_clip_list(offset, limit):
        """
        Return a URL used to get a basic video list, with optional offset and
        limit parameters for pagination
        """


class IAPISettings(Interface):
    """
    Global API settings
    """

    url_base = schema.TextLine(
        title=_(u"URL Base"),
        description=_(u"Base URL for the API."),
        required=True,
        default=u"http://multimedia.tlsur.net/api/",
        )

    video_api = schema.TextLine(
        title=_(u"Video API"),
        description=_(u"API to interact with the video."),
        required=True,
        default=u"clip/?",
        )

    video_api_regex_string = schema.TextLine(
        title=_(u"Video API Regex string"),
        description=_(u"Regex to match with the video API."),
        required=True,
        default=u"^http:\/\/.+\/api\/(?P<url>clip\/.+?)$",
        )

    video_widget_url_base = schema.TextLine(
        title=_(u"Video widget URL base"),
        description=_(u""),
        required=True,
        default=u"http://multimedia.telesurtv.net/player/insertar.js?archivo=",
        )

    video_regex_string = schema.TextLine(
        title=_(u"Video Regex string"),
        description=_(u"Regex to match with videos from the API."),
        required=True,
        default=u"^http:\/\/.+\/(?P<url>clips\/.+\.mp4?)$",
        )

    audio_regex_string = schema.TextLine(
        title=_(u"Audio Regex string"),
        description=_(u"Regex to match with the audio API."),
        required=True,
        default=u"^http:\/\/.+\/(?P<url>clips\/.+\.mp3?)$",
        )

    most_seen_widget = schema.TextLine(
        title=_(u"Most seen video widget"),
        description=_(u"A widget for the videos most seen"),
        required=True,
        default=u"http://multimedia.telesurtv.net/media/video/cmswidgets/cmswidgets.html?widget=mas_vistos",
        )

    latest_from_section_widget = schema.TextLine(
        title=_(u"Latest video widget from section"),
        description=_(u"A widget that will show the latest video from a given section"),
        required=True,
        default=u"http://multimedia.telesurtv.net/media/video/cmswidgets/videos.html?widget=ultimos_seccion",
        )

    time_filter_day = schema.TextLine(
        title=_(u"Filter results by day"),
        description=_(u""),
        required=True,
        default=u"tiempo=dia",
        )

    time_filter_week = schema.TextLine(
        title=_(u"Filter results by week"),
        description=_(u""),
        required=True,
        default=u"tiempo=semana",
        )

    time_filter_month = schema.TextLine(
        title=_(u"Filter results by month"),
        description=_(u""),
        required=True,
        default=u"tiempo=mes",
        )

    time_filter_year = schema.TextLine(
        title=_(u"Filter results by year"),
        description=_(u""),
        required=True,
        default=u"tiempo=ano",
        )

    video_thumbnail_small = schema.TextLine(
        title=_(u"Small thumbnail"),
        description=_(u"Get the small thumbnail from the returned JSON"),
        required=True,
        default=u"thumbnail_pequeno",
        )

    video_thumbnail_medium = schema.TextLine(
        title=_(u"Medium thumbnail"),
        description=_(u"Get the medium thumbnail from the returned JSON"),
        required=True,
        default=u"thumbnail_mediano",
        )

    video_thumbnail_large = schema.TextLine(
        title=_(u"Large thumbnail"),
        description=_(u"Get the large thumbnail from the returned JSON"),
        required=True,
        default=u"thumbnail_grande",
        )

    audio_only = schema.TextLine(
        title=_(u"Audio only"),
        description=_(u"Only get audio"),
        required=True,
        default=u"solo_audio=true",
        )

    offset = schema.TextLine(
        title=_(u"Offset"),
        description=_(u"Specify the offset for pagination"),
        required=True,
        default=u"offsset",
        )

    limit = schema.TextLine(
        title=_(u"Limit"),
        description=_(u"Specify the number of items to retrieve"),
        required=True,
        default=u"limit",
        )

    details = schema.TextLine(
        title=_(u"Details"),
        description=_(u"Specify the level of info to retrieve"),
        required=True,
        default=u"detalle",
        )
