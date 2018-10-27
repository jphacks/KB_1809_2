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

    def to_internal_value(self, data):
        plan_id = data.get('plan_id')
        text = data.get('text')
        if not plan_id:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        if not text or len(text) == 0:
            raise serializers.ValidationError({'text': 'This field is required.'})

        return {
            'user': self.context['request'].user,
            'plan_id': plan_id,
            'text': text,
        }
