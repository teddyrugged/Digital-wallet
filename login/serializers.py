from rest_framework import serializers
from authentication.models import (User, Currency, Wallet)

##########################
'''UserSerializer'''


##########################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','last_login','date_joined','otp','created_at','updated_at', 'groups', 'user_permissions']
        # fields = "__all__"
        # exclude = ('watchlist',)


##########################
'''CurrencySerializer'''


##########################

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"
        # exclude = ('watchlist',)


##########################
''' WalletSerializer'''


##########################

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        # exclude = ('watchlist',)
