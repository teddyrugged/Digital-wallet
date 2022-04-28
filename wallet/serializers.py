from rest_framework import serializers

from authentication.models import Wallet, Currency


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'currency_id', 'amount']
        # exclude = ('username_id',)

    def create(self, validated_data):
        validated_data['username_id'] = self.context['username_id']
        return Wallet.objects.create(**validated_data)


class FundWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'amount', 'currency_id']


class WithdrawWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'amount', 'currency_id']
