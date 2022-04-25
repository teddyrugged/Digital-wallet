from rest_framework import generics, permissions

from . import serializers
from .models import Wallet


class WalletApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WalletSerializers
    queryset = Wallet.objects.all()
