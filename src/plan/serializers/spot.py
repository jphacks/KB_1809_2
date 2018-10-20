from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from plan.models import Spot
from .base import BaseListSerializer

import datetime


class SpotListSerializer(BaseListSerializer):
    """
    Spotを複数処理するserializer
    """

    def create(self, validated_data):
        spots = list()
        for i, s in enumerate(validated_data):
            created_at = datetime.datetime.now()
            new_spot = Spot(**s, order=i, created_at=created_at)
            spots.append(new_spot)

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
        ordering = ("order",)
