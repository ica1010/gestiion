from django.contrib import admin
from django.urls import path

from userauth.views import *

urlpatterns = [
    path('add-user/', add_user, name='sign-up'),
    path('sign-in/', login_view, name='sign-in'),
    path('sign-out/', logout_view, name='sign-out'),
    path('me/', Profile, name='me'),
]