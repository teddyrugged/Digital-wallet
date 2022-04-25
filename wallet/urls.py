from django.urls import path

from . import views

urlpatterns = [
    path('wallets/', views.WalletApiView.as_view(), name='wallets'),
]
