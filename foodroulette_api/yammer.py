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
    return self.connection.users.find(user_id)

  def get_my_user(self):
    return self.connection.users.find_current()


def get_token(code):
  authenticator = yampy.Authenticator(client_id=YAMMER_ID,
                                      client_secret=YAMMER_SECRET)
  return authenticator.fetch_access_token(code)
