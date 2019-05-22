from django.urls import path

from . import views


urlpatterns = [
    path('accounts/', views.AccountView.as_view(), name='account'),
    path('friends/', views.AllFriendsListView.as_view(), name='all_friends'),
    path('friends/<str:account>/', views.FriendsListView.as_view(), name='friends'),
]
