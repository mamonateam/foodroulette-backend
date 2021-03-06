from foodroulette_api.base_resource import BaseResource
from foodroulette_api.models import *
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.http import *
import json
from django.http import HttpResponse
from foodroulette_api.roulette_logic import *
from foodroulette_api.bing import *


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

            url(r"^(?P<resource_name>%s)/exec%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('roulette_exec'), name="api_roulette_exec"),
           ]


  def roulette_info(self, request, **kwargs):
    self.is_authenticated(request)
    is_ready = is_roulette_ready()

    token_md5 = request.GET['token_md5']
    db_user = User.objects.get(token_md5=token_md5)

    user_ids = []

    if (db_user.roulette):
      user_ids = map(lambda x: x.yammer_id, db_user.roulette.user_set.exclude(id=db_user.id))

    return self.create_response(request, {"is_ready": is_ready,
                                          "user_ids": user_ids})


  def roulette_exec(self, request, **kwargs):
    exec_roulette()
    return self.create_response(request, {'result': 'Roulettes executed.'})


  def roulette_clean(self, request, **kwargs):
    clean_roulette()
    return self.create_response(request, {'result': 'All roulettes have been cleant'})



#************************************************************************
# Message Resource
#************************************************************************
class MessageResource(BaseResource):
  class Meta(BaseResource.Meta):
    resource_name = 'message'


  def prepend_urls(self):
    return [url(r"^(?P<resource_name>%s)%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('send_message'), name="api_send_message"),
           ]


  def send_message(self, request, **kwargs):
    self.is_authenticated(request)
    token_md5 = request.GET['token_md5']
    data = json.loads(request.body)
    id_to = int(data['user_id'])
    body = data['body']
    db_user = User.objects.get(token_md5=token_md5)
    yammer = Yammer(db_user.token)

    yammer.send_message(id_to, body)
    return self.create_response(request, {'result': 'Message sent ok.'})



#************************************************************************
# News Resource
#************************************************************************
class NewsResource(BaseResource):
  class Meta(BaseResource.Meta):
    resource_name = 'news'


  def prepend_urls(self):
    return [url(r"^(?P<resource_name>%s)/(?P<user_id>\d*)%s$" % 
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('get_news'), name="api_get_news"),
           ]

  def get_news(self, request, user_id, **kwargs):
    self.is_authenticated(request)
    token_md5 = request.GET['token_md5']
    user_id = int(user_id)

    db_user = User.objects.get(token_md5=token_md5)
    yammer = Yammer(db_user.token)
    yammer_user = yammer.get_user(user_id)

    i = 0
    news = []

    while i < 3 and i < len(yammer_user['interests']):
      term = yammer_user['interests'][i]
      new = {'title': '', 'url': ''}

      try:
        bs = Bing(term)
        title, url = bs.do_search()
        new['title'] = title
        new['url'] = url
      except:
        pass

      news.append(new)
      i += 1

    return self.create_response(request, news)
