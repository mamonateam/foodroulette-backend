import yampy

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

