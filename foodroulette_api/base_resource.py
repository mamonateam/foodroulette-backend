from tastypie.resources import ModelResource
from tastypie.exceptions import ImmediateHttpResponse

#************************************************************************
# Base Resource
#************************************************************************
class BaseResource(ModelResource):
  class Meta:
    always_return_data = True
    include_resource_uri = False

  def is_authenticated(self, request):
    # TODO!!
    return True