from tastypie.resources import ModelResource
from tastypie.exceptions import ImmediateHttpResponse
from foodroulette_api.models import *
from tastypie.http import HttpForbidden
from tastypie.authorization import Authorization


#************************************************************************
# Base Resource
#************************************************************************
class BaseResource(ModelResource):
  class Meta:
    always_return_data = True
    include_resource_uri = False
    authorization= Authorization()

  def is_authenticated(self, request):
    if ('token_md5' in request.GET and
        User.objects.filter(token_md5=request.GET['token_md5'])):
      return True
    else:
      raise ImmediateHttpResponse(HttpForbidden("These are not the droids you're looking for..."))
