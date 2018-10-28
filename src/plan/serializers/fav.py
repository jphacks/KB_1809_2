from rest_framework import serializers

from plan.models import Plan

from accounts.serializers import SimpleUserSerializer
from plan.models import Fav
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

    user = SimpleUserSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(read_only=True)

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
        return {
            'plan_id': data['plan_id'],
        }

    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))
        fav, is_created = Fav.objects.get_or_create(user=user, plan=plan)
        if not is_created:
            raise serializers.ValidationError({'plan_id': 'already favorite'})
        return fav

    def to_representation(self, instance):
        data = super(FavSerializer, self).to_representation(instance)
        if self.context['request'].version == 'v2':
            data['created_at'] = int(instance.created_at.strftime('%s'))
        return data
