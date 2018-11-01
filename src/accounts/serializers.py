from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import User


class UserSerializer(serializers.ModelSerializer):
    icon = Base64ImageField()

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'created_at', 'icon', 'updated_at')


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'icon')


class CreateUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, email):
        if len(email) == 0:
            raise serializers.ValidationError({'email': 'Do not allow to use empty email'})
        return email

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, is_active=True)
