from django.urls import include, path
from .views import (UserListCreateAPIView,UserRetrieveUpdateDestroyAPIView,CurrencyListCreateAPIView,CurrencyRetrieveUpdateDestroyAPIView, WalletListCreateAPIView,WalletRetrieveUpdateDestroyAPIView)
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    #User
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    
    #Currency
    path('currency/', CurrencyListCreateAPIView.as_view(), name='currency-list'),
    path('currency/<int:pk>/', CurrencyRetrieveUpdateDestroyAPIView.as_view(), name='currency-detail'),
    
    #Wallet
    path('wallet/', WalletListCreateAPIView.as_view(), name='wallet-list'),
    path('wallet/<int:pk>/', WalletRetrieveUpdateDestroyAPIView.as_view(), name='wallet-detail'),
    
    #RestFramework interface login/logout option
    path('api-auth', include('rest_framework.urls')),
    
    #JWT Login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    
    ]