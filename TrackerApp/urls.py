from .views import *
from django.urls import path

urlpatterns = [
    path('signup/', signUp, name='sign_up'),
    path('signin/', signIn, name='sign_in'),
    path('dashboard/', dashboard, name='dashboard'),
    path('signout/', signOut, name='sign_out'),
    path('watchlists/', watchLists, name='watch_lists'),
    path('watchlist/<int:pk>/', watchList, name='watch_list'),
]