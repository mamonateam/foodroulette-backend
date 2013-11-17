from django.db import models
from foodroulette_api.yammer import Yammer
from foodroulette_api.misc import md5_hash

""""
FoodRoulette Models
"""

#************************************************************************
# Roulette  
#************************************************************************
class Roulette(models.Model):
  pass


#************************************************************************
# Food Preference 
#************************************************************************
class FoodPreference(models.Model):
  name = models.CharField(max_length=200, unique=True, 
                          db_index=True)



#************************************************************************
# User  
#************************************************************************
class User(models.Model):
  yammer_id = models.CharField(max_length=255, unique=True,
                               db_index=True)
  token = models.CharField(max_length=255, unique=True,
                           db_index=True)
  token_md5 = models.CharField(max_length=32, unique=True, 
                               db_index=True)
  is_eating = models.BooleanField(default=False, 
                                  db_index=True)
  food_preferences = models.ManyToManyField(FoodPreference, blank=True, 
                                            null=True)
  roulette = models.ForeignKey(Roulette, null=True,
                               on_delete=models.SET_NULL)



def create_user(token):
  yammer = Yammer(token)
  user_dict = yammer.get_my_user()

  u = User.objects.filter(token=token)
  if u:
    u = u[0]
  else:
    u = User(yammer_id=user_dict['id'],
             token=token,
             token_md5=md5_hash(token))
    u.save()
  return u