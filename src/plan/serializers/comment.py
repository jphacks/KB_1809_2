from rest_framework import serializers

from plan.models import Comment, Plan
from accounts.models import User

from accounts.serializers import SimpleUserSerializer
from .base import BaseListSerializer


class CommentListSerializer(BaseListSerializer):
    """
    複数のコメントを処理するSerializer
    """

    def create(self, validated_data):
        comments = [Comment(**item) for item in validated_data]
        return Comment.objects.bulk_create(comments)


class CommentSerializer(serializers.ModelSerializer):
    """
    単一のCommentを処理するSerializer
    """

    user = SimpleUserSerializer()
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = Comment
        fields = ("pk", "user", "plan_id", "text")
        list_serializer_class = CommentListSerializer

    def validate(self, attrs):
        """必要フィールドを含んでいるかのバリデーション"""
        fields = ('plan_id', 'text')
        for key in fields:
            if key not in attrs:
                raise serializers.ValidationError({key: "This field is required."})
        return attrs

    def to_internal_value(self, data):
        if len(data['text']) == 0:
            raise serializers.ValidationError({'text': "Please input text."})
        return {
            'plan_id': data['plan_id'],
            'text': data['text']
        }

    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))
        text = validated_data.get('text')

        return Comment.objects.create(user=user, plan=plan, text=text)
