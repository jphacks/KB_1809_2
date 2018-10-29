from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from plan.models import Report, Plan

from accounts.serializers import SimpleUserSerializer
from .base import BaseListSerializer


class ReportListSerializer(BaseListSerializer):
    """
    複数のReportを処理するSerializer
    """

    def create(self, validated_data):
        reports = [Report(**item) for item in validated_data]
        return Report.objects.bulk_create(reports)


class ReportSerializer(serializers.ModelSerializer):
    """
    単一のReportを処理するSerializer
    """

    image = Base64ImageField()
    user = SimpleUserSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = ("pk", "user", "plan_id", "image", "text", "created_at")
        list_serializer_class = ReportListSerializer

    def to_representation(self, instance):
        data = super(ReportSerializer, self).to_representation(instance)
        if self.context['request'].version == 'v2':
            data['created_at'] = int(instance.created_at.strftime('%s'))
        return data

    def validate(self, attrs):
        """必要フィールドを含んでいるかのバリデーション"""
        field = ('plan_id', 'image', 'text')
        for key in field:
            if key not in attrs:
                raise serializers.ValidationError({key: "This field is required."})
        return attrs

    def to_internal_value(self, data):
        data['user'] = self.context['request'].user
        data['plan'] = Plan.objects.get(pk=data.get('plan_id'))
        b64image = data.pop('image')
        if len(b64image) != 0:
            data['image'] = Base64ImageField().to_internal_value(b64image)
        return data
