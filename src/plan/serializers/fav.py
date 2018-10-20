from rest_framework import serializers

from plan.models import Fav, Plan
from accounts.models import User

from .user import SimpleUserSerializer


class FavSerializer(serializers.ModelSerializer):
    """
    単一のFavを処理するSerializer
    """

    user = SimpleUserSerializer()
    plan = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Fav
        field = ("pk", "user", "plan")

    def to_internal_value(self, data):
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')
        if not user_id:
            raise serializers.ValidationError({'user_id': 'This field is required.'})
        if not plan_id:
            raise serializers.ValidationError({'plan_id': 'This field is required.'})
        return {
            'user_id': user_id,
            'plan_id': plan_id,
        }

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data.get('user_id'))
        plan = Plan.objects.get(pk=validated_data.get('plan_id'))

        return Fav.objects.create(user=user, plan=plan)

