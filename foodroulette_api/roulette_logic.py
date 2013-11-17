from foodroulette_api.models import *
from foodroulette_backend.settings import *
import random

def clean_roulette():
  Roulette.objects.all().delete()

  for u in User.objects.all():
    u.is_eating = not u.yammer_id in DEMO_USERS_IDS
    u.save()



def is_roulette_ready():
  return not not Roulette.objects.count()


def exec_roulette():
  users_hashed_by_id = {}
  r = None

  for u in User.objects.all():
    users_hashed_by_id[u.id] = u

  user_ids = users_hashed_by_id.keys()


  # Execute roulette
  while len(user_ids) > 2:
    r = Roulette.objects.create()

    first_id = user_ids[random.randrange(0, len(user_ids))]
    user_ids.remove(first_id)
    first_user = users_hashed_by_id[first_id]
    first_user.roulette_id = r.id
    first_user.save()

    second_id = user_ids[random.randrange(0, len(user_ids))]
    user_ids.remove(second_id)
    second_user = users_hashed_by_id[second_id]
    second_user.roulette_id = r.id
    second_user.save()

    third_id = user_ids[random.randrange(0, len(user_ids))]
    user_ids.remove(third_id)
    third_user = users_hashed_by_id[third_id]
    third_user.roulette_id = r.id
    third_user.save()

  # if they're not multiple of 3
  if not r:
    r = Roulette.objects.create()
  
  for user_id in user_ids:
    user = users_hashed_by_id[user_id]
    user.roulette_id = r.id
    user.save()

