from rest_framework import serializers

from plan.models import Plan
from .spot import SpotSerializer
from .fav import FavSerializer
from .comment import CommentSerializer
from .report import ReportSerializer
from .location import LocationSerializer
from accounts.serializers import SimpleUserSerializer


class AbstractPlanSerializer(serializers.ModelSerializer):
    """
    List表示用のPlanSerializer
    """
    spots = SpotSerializer(many=True, allow_null=True)
    user = SimpleUserSerializer()
    location = LocationSerializer()

    class Meta:
        model = Plan
        fields = ('pk', 'name', 'price', 'duration', 'note', 'location', 'spots',
                  'created_at', 'user', 'favorite_count', 'comment_count')

    def to_representation(self, instance):
        res = super(AbstractPlanSerializer, self).to_representation(instance)
        all_spots = res['spots']
        res['spots'] = [all_spots[0], all_spots[-1]]
        return res


class PlanSerializer(serializers.ModelSerializer):
    """
    単一のPlanの処理
    """

    spots = SpotSerializer(many=True, allow_null=True)
    favs = FavSerializer(many=True, allow_null=True)
    comments = CommentSerializer(many=True, allow_null=True)
    reports = ReportSerializer(many=True, allow_null=True)
    user = SimpleUserSerializer()
    location = LocationSerializer()

    class Meta:
        model = Plan
        fields = ('pk', 'name', 'price', 'duration', 'note', 'location',
                  'reports', 'favs', 'created_at', 'comments', 'spots', 'user',
                  'favorite_count', 'comment_count')
