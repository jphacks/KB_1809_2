from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from plan.models import Spot, Plan
from .base import BaseListSerializer


class SpotListSerializer(BaseListSerializer):
    """
    Spotを複数処理するserializer
    """

    def create(self, validated_data):
        spots = list()
        for i, s in enumerate(validated_data):
            s['order'] = i
            new_spot = self.child.create(s)
            spots.append(new_spot)

        return spots


class SpotSerializer(serializers.ModelSerializer):
    """
    単一のSpotを処理するSerializer
    """

    image = Base64ImageField()
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), read_only=False)

    class Meta:
        model = Spot
        fields = ("pk", "name", "order", "lat", "lon", "note", "plan_id", "image", "created_at")
        list_serializer_class = SpotListSerializer

    def create(self, validated_data):
        plan = validated_data.pop('plan_id')
        return Spot.objects.create(**validated_data, plan=plan)

    def to_representation(self, instance):
        created_at = instance.created_at
        data = super(SpotSerializer, self).to_representation(instance)
        if self.context['request'].version == 'v2':
            created_at = created_at.strftime('%s')
            data['created_at'] = int(created_at)
        return data
