from foodroulette_api.base_resource import BaseResource
from foodroulette_api.models import *
from foodroulette_api.yammer import get_token
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.http import *
import json
from django.shortcuts import redirect




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
    self.method_check(request, allowed=['get'])

    code = request.GET['code']
    token = get_token(code)
    user = create_user(token)
    token_md5 = user.token_md5

    return redirect('#/login/%s' % token_md5)



#************************************************************************
# Roulette Resource
#************************************************************************

# TODO