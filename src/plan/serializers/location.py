from rest_framework import serializers

from plan.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("pk", "p_name", "p_code", "m_name", "m_code")

    def to_internal_value(self, data):
        res = {}
        for key in self.Meta.fields:
            if key == 'pk':
                continue
            if key not in data:
                raise serializers.ValidationError({key: 'This field is required'})
            res[key] = data.get(key)
        return res

    def create(self, validated_data):
        loc, _ = Location.objects.get_or_create(**validated_data)
        return loc
