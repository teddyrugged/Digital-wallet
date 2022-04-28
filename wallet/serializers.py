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

    def validate(self, attrs):
        amount = attrs.get('amount', '')
        user = self.context['details'][0]
        wallet_owner = Wallet.objects.get(pk=self.context['details'][1]).username_id

        if not amount:
            raise serializers.ValidationError('Amount should not be empty')
        if user != wallet_owner:
            raise serializers.ValidationError('You are not the owner of this Wallet! You cannot fund this wallet')
        return super().validate(attrs)


class WithdrawWalletSerializers(FundWalletSerializers):
    class Meta:
        model = Wallet
        fields = ['id', 'amount', 'currency_id']
