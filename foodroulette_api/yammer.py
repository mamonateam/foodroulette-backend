import yampy
from foodroulette_backend.settings import *

""""
Convenience class to deal with Yammer API
"""
class Yammer(object):

  def __init__(self, token):
    self.token = token
    self.connection = yampy.Yammer(access_token=self.token)


  def get_user(self, user_id):
    return self.__serializate_user(self.connection.users.find(user_id))


  def get_my_user(self):
    return self.__serializate_user(self.connection.users.find_current())


  def update_interests(self, user_id, interests):
    str_interests = ', '.join(interests)
    self.connection.users.update(user_id, interests=str_interests)


  def send_message(self, user_id, body):
    self.connection.messages.create(body=body, direct_to_id=user_id)


  def __serializate_user(self, user):
    if user['interests']:
      user['interests'] = map(lambda x: x.strip(), user['interests'].split(','))
    return user



def get_token(code):
  authenticator = yampy.Authenticator(client_id=YAMMER_ID,
                                      client_secret=YAMMER_SECRET)
  return authenticator.fetch_access_token(code)
