from rest_framework import serializers

from plan.models import Plan
from .spot import SpotSerializer
from .fav import FavSerializer
from .comment import CommentSerializer
from .report import ReportSerializer
from .location import LocationSerializer


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
