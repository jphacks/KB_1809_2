from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from plan.models import Report, Plan
from accounts.models import User

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
    user = SimpleUserSerializer()
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = Report
        fields = ("pk", "user", "plan_id", "image", "text")
        list_serializer_class = ReportListSerializer

    def to_internal_value(self, data):
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        image = data.get('image')
        text = data.get('text')
        if not user_id:
            raise serializers.ValidationError({'user_id': 'This field is required.'})
        if not plan_id:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        if not image:
            raise serializers.ValidationError({'image': 'This field is required.'})
        if not text:
            raise serializers.ValidationError({'text': 'This field is required.'})

        return {
            'user_id': user_id,
            'plan_id': plan_id,
            'image': image,
            'text': text,
        }

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data.get('user_id'))
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))
        image = validated_data.get('image')
        text = validated_data.get('text')

        return Report.objects.create(user=user, plan=plan, image=image, text=text)
