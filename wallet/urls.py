from django.urls import path

from . import views

urlpatterns = [
    path('wallets/', views.WalletApiView.as_view(), name='wallets'),
    path('fund/<int:pk>/', views.FundWalletApiView.as_view(), name='fund'),
]
