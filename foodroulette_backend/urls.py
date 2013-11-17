from django.conf.urls import patterns, include, url
from foodroulette_api.views import *

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from foodroulette_api.api import *
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RouletteResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foodroulette_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^user_register/', 'foodroulette_api.views.user_register'),
)