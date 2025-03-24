from django.urls import re_path
from apps.chat import consumers, views



websocket_urlpatterns = [
	re_path(r'ws/users/(?P<userId>\w+)/chat/$',consumers.ChatConsumer.as_asgi()),
	re_path(r'',views.HandleUnexpectedCall.as_view(),
	),
		
]
