from foodroulette_api.base_resource import BaseResource
from foodroulette_api.models import *
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.http import *



"""
FoodRoulette API
"""



#************************************************************************
# User Resource
#************************************************************************
class UserResource(BaseResource):
  class Meta(BaseResource.Meta):
    resource_name = 'user'


  def prepend_urls(self):
    return [url(r"^(?P<resource_name>%s)%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('user_register'), name="api_user_register"),
           ]

  def user_register(self, request, **kwargs):
    return self.create_response(request, {'test': 'It works! :)'})


#************************************************************************
# Roulette Resource
#************************************************************************

# TODO