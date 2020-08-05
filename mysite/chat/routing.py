from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/quixx/(?P<game_name>\w+)/$', consumers.QuixxGameConsumer),
]
