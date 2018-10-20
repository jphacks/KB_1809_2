from rest_framework import serializers


from plan.models import Location
from plan.geo import convert_geo_to_location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("pk", "p_name", "p_code", "m_name", "m_code")

    def to_internal_value(self, data):
        lat = data.get('lat')
        lon = data.get('lon')
        if not lat:
            raise serializers.ValidationError({'lat': 'This fields is required.'})
        if not lon:
            raise serializers.ValidationError({'lon': 'This fields is required.'})
        return {
            'lat': lat,
            'lon': lon,
        }

    def create(self, validated_data):
        loc = convert_geo_to_location(**validated_data)
        return Location.objects.create(
            p_name=loc.p_name,
            p_code=loc.p_code,
            m_name=loc.m_name,
            m_code=loc.m_code,
        )

