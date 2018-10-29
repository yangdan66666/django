from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'file_operation.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^land/',include('land.urls')),
    url(r'^upload/',include('upload.urls')),
    url(r'^other/',include('other.urls')),
]
