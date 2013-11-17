from foodroulette_api.models import *

def clean_roulette():
  Roulette.objects.all().delete()

  for u in User.objects.all():
    u.is_eating = False
    u.save()
