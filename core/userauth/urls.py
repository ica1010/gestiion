from django.contrib import admin
from django.urls import path

from userauth.views import *

urlpatterns = [
    path('sign-up/', register_view, name='sign-up'),
    path('sign-in/', login_view, name='sign-in'),
    path('sign-out/', logout_view, name='sign-out'),
]