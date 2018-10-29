from django.conf.urls import url
from .views import *
urlpatterns = [
	url(r'^wother',wother_views),
	url(r'^other',other_views),
	url(r'^open',open_views),
	]