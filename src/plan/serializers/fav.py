from rest_framework import serializers

from plan.models import Fav, Plan

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
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = Fav
        fields = ("pk", "user", "plan_id")
        list_serializer_class = FavListSerializer

    def validate(self, attrs):
        """必要フィールドを含んでいるかのバリデーション"""
        if 'plan_id' not in attrs:
            raise serializers.ValidationError({'plan_id': "This field is required."})
        return attrs

    def to_internal_value(self, data):
        plan_id = data.get('plan_id')
        if not plan_id:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        return {
            'plan_id': plan_id,
        }

    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))
        return Fav.objects.create(user=user, plan=plan)
