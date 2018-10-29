from django.conf.urls import url
from .views import *
urlpatterns = [
	url(r'^$',login_views),
	url(r'^login$',login_views),
	url(r'^register$',register_views),
	]