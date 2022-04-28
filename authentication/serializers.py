from random import randint

from django.conf import settings
from django.shortcuts import reverse
from rest_framework import serializers

from authentication.models import User, Wallet
from .utils import Utils


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'main_currency', 'token')

        read_only_fields = ['token']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
            raise serializers.ValidationError({username, 'Username already in use'}, {email, 'Email already in use'})
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError({email, 'Email already in use'})
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError({username, 'Username already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()

        cur_instance = new_user.main_currency

        Wallet.objects.create(username_id=new_user, currency_id=cur_instance,
                              name=f'{new_user.first_name} {cur_instance.name} Wallet').save()
        return new_user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'token')

        read_only_fields = ['token']


class MyResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def generate_otp(self):
        return randint(1000, 9999)

    def validate(self, attrs):
        try:
            email = attrs.get('email', '')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

                user.otp = self.generate_otp()
                user.save()

                token = user.token

                relative_link = reverse('reset-password')
                data = {
                    'subject': 'Reset Link',
                    'body': f"This is a message to reset your password. Your token is: {user.otp} and the link to click is: {settings.BASE_URL}{relative_link}?token={token} ",
                    'receiver': email
                }

                Utils.send_email(data)

        except Exception as err:
            print('WAHALA', err)
            raise Exception(str(err))
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=1, max_length=100, write_only=True)
    token = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        fields = ['password', 'token']

    def validate(self, attrs):
        return super().validate(attrs)


class ValidateOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    def validate(self, attrs):
        return super().validate(attrs)
