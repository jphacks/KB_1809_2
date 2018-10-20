from rest_framework import serializers

from plan.models import Fav, Plan
from accounts.models import User

from accounts.serializers import SimpleUserSerializer
from .base import BaseListSerializer


class FavListSerializer(BaseListSerializer):
    """
    複数のFavを処理するSerializer
    """

    def create(self, validated_data):
        favs = [Fav(**item) for item in validated_data]
        return Fav.objects.bulk_create(favs)


class FavSerializer(serializers.ModelSerializer):
    """
    単一のFavを処理するSerializer
    """

    user = SimpleUserSerializer()
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = Fav
        fields = ("pk", "user", "plan")
        list_serializer_class = FavListSerializer

    def to_internal_value(self, data):
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        if not user_id:
            raise serializers.ValidationError({'user_id': 'This field is required.'})
        if not plan_id:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        return {
            'user_id': user_id,
            'plan_id': plan_id,
        }

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data.get('user_id'))
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))
        return Fav.objects.create(user=user, plan=plan)
