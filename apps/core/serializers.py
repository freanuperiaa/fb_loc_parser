from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Account, Friend


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password')


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = (
            'name', 'current_city', 'hometown', 'friend_of')
