from foodroulette_api.base_resource import BaseResource
from foodroulette_api.models import *
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.http import *
import json
from django.http import HttpResponse
from foodroulette_api.roulette_logic import *

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
    return [url(r"^(?P<resource_name>%s)/me%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('user_me'), name="api_user_me"),

            url(r"^(?P<resource_name>%s)%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('user_info'), name="api_user_info"),

            url(r"^(?P<resource_name>%s)/(?P<user_id>\d*)%s$" %
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('get_user'), name="api_get_user"),
           ]


  def user_info(self, request, **kwargs):
    return self.create_response(request, {'options': '[/me, /id]'})


  def user_me(self, request, **kwargs):
    self.is_authenticated(request)

    if (len(request.body)):
      # update my user
      return self.update_my_user(request)
    else:
      # return my user
      return self.return_my_user(request)


  def return_my_user(self, request):
    token_md5 = request.GET['token_md5']
    db_user = User.objects.get(token_md5=token_md5)
    yammer = Yammer(db_user.token)
    yammer_user = yammer.get_my_user()
    db_user.add_foodroulette_fields(yammer_user)

    return self.create_response(request, yammer_user)


  def update_my_user(self, request):
    token_md5 = request.GET['token_md5']
    client_user = json.loads(request.body)

    # Update is_eating and food_preferences (DB)
    db_user = User.objects.get(token_md5=token_md5)
    db_user.is_eating = client_user['food_roulette']['is_eating']
    db_user.update_food_preferences(client_user['food_roulette']['food_preferences'])
    db_user.save()

    # Update interests (Yammer)
    yammer = Yammer(db_user.token)
    yammer_user = yammer.get_my_user()
    yammer.update_interests(yammer_user['id'], client_user['interests'])

    return self.create_response(request, client_user)


  def get_user(self, request, user_id, **kwargs):
    self.is_authenticated(request)

    db_user = User.objects.get(yammer_id=user_id)
    yammer = Yammer(db_user.token)
    yammer_user = yammer.get_user(int(user_id))
    db_user.add_foodroulette_fields(yammer_user)

    return self.create_response(request, yammer_user)




#************************************************************************
# Roulette Resource
#************************************************************************
class RouletteResource(BaseResource):
  class Meta(BaseResource.Meta):
    resource_name = 'roulette'


  def prepend_urls(self):
    return [ url(r"^(?P<resource_name>%s)%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('roulette_info'), name="api_roulette_info"),

            url(r"^(?P<resource_name>%s)/clean%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('roulette_clean'), name="api_roulette_clean"),
           ]


  def roulette_info(self, request, **kwargs):
    return self.create_response(request, {'options': '[/, /exec, /clean]'})


  def roulette_clean(self, request, **kwargs):
    clean_roulette()
    return self.create_response(request, {'result': 'Roulette has been cleant'})
