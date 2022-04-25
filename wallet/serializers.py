from rest_framework import serializers

from .models import Wallet


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        exclude = ('username_id',)
