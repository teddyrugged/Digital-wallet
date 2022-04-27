from rest_framework import serializers

from .models import Wallet, Currency


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        exclude = ('username_id',)

    def create(self, validated_data):
        validated_data['username_id'] = self.context['username_id']
        return Wallet.objects.create(**validated_data)


class FundWalletSerializers(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['amount', 'currency_id']
