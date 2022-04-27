from django.shortcuts import render
from authentication.models import (User, Currency, Wallet)
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from .serializers import (UserSerializer, CurrencySerializer, WalletSerializer)

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (IsAdminUser, IsAuthenticated)
from .permissions import (AdminOrAuthenticatedReadOnly)

##########################
'''User Views'''
##########################

class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    # authentication_classes = [SessionAuthentication,TokenAuthentication]
    # permission_classes = [AllowAny,IsAuthenticated,IsAdminUser]   


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    # authentication_classes = [SessionAuthentication,TokenAuthentication]
    # permission_classes = [AllowAny,IsAuthenticated,IsAdminUser]  


##########################
'''Currency Views'''
##########################

class CurrencyListCreateAPIView(ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    permission_classes = [IsAdminUser]  

    # authentication_classes = [SessionAuthentication,TokenAuthentication]
    # permission_classes = [AllowAny,IsAuthenticated,IsAdminUser]  


class CurrencyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    permission_classes = [IsAdminUser] 

    # authentication_classes = [SessionAuthentication,TokenAuthentication]
    # permission_classes = [AllowAny,IsAuthenticated,IsAdminUser]    


##########################
'''Wallet Views'''
##########################

class WalletListCreateAPIView(ListCreateAPIView):
    queryset = Wallet.objects.all()

    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    # authentication_classes = [SessionAuthentication,TokenAuthentication]
    # permission_classes = [AllowAny,IsAuthenticated,IsAdminUser]    


class WalletRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    permission_classes = [IsAuthenticated]
  
    # authentication_classes = [SessionAuthentication,TokenAuthentication]
    # permission_classes = [AllowAny,IsAuthenticated,IsAdminUser]
