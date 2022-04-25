from rest_framework import serializers

from .models import Wallet


class WalletSerializers(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        exclude = ('username_id',)

    def create(self, validated_data):
        validated_data['username_id'] = self.context['username_id']
        return Wallet.objects.create(**validated_data)
