from django.conf.urls import patterns, include, url
from foodroulette_api.views import *

from django.contrib import admin
admin.autodiscover()

# API Endpoints
from foodroulette_api.api import *
user_resource = UserResource()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foodroulette_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(user_resource.urls)),
    url(r'^user_register/', 'foodroulette_api.views.user_register'),
)