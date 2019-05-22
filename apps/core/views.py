from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import AccountSerializer, UserSerializer, FriendSerializer
from .models import Account, Friend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class AccountView(APIView):

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # call spider here!!!
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class AllFriendsListView(APIView):
    def get(self, request, format=None):
        friends = Friend.objects.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)


class FriendsListView(APIView):
    def get(self, request, account, format=None):
        account = self.kwargs['account']
        friends = Friend.objects.filter(friend_of__email=account)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)
