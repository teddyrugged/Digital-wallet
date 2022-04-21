from rest_framework import serializers

from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

        read_only_fields = ['token']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'token')

        read_only_fields = ['token']
