from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from plan.models import Spot
from .base import BaseListSerializer


class SpotListSerializer(BaseListSerializer):
    """
    Spotを複数処理するserializer
    """

    def create(self, validated_data):
        spots = [Spot(**item) for item in validated_data]
        return Spot.objects.bulk_create(spots)


class SpotSerializer(serializers.ModelSerializer):

    """
    単一のSpotを処理するSerializer
    """

    image = Base64ImageField()

    class Meta:
        model = Spot
        fields = ("pk", "name", "order", "lat", "lon", "note", "image", "created_at")
        list_serializer_class = SpotListSerializer
