from rest_framework import serializers

from plan.models import Comment, Plan
from accounts.models import User

from accounts.serializers import SimpleUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    単一のCommentを処理するSerializer
    """

    user = SimpleUserSerializer()
    plan = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Comment
        fields = ("pk", "user", "plan", "text")

    def to_internal_value(self, data):
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        text = data.get('text')
        if not user_id:
            raise serializers.ValidationError({'user_id': 'This field is required.'})
        if not plan_id:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        if not text or len(text) == 0:
            raise serializers.ValidationError({'text': 'This field is required.'})

        return {
            'user_id': user_id,
            'plan_id': plan_id,
            'text': text,
        }

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data.get('user_id'))
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))
        text = validated_data.get('text')

        return Comment.objects.create(user=user, plan=plan, text=text)
