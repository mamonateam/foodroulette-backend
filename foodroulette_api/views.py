from django.shortcuts import render
from django.shortcuts import redirect
from foodroulette_api.yammer import get_token
from foodroulette_api.models import *


def user_register(request):
  code = request.GET['code']
  token = get_token(code)
  user = create_user(token)
  token_md5 = user.token_md5

  return redirect('http://localhost:9000/#/login/%s' % token_md5)