from rest_framework import serializers

from accounts.models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    シンプルなUserを処理するSerializer
    """

    class Meta:
        model = User
        fields = ("pk", "name")
