from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import User


class UserSerializer(serializers.ModelSerializer):
    icon = Base64ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'created_at', 'icon', 'updated_at')


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'icon')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_active=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
