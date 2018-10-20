from rest_framework import serializers

from plan.models import Plan, Spot, Location
from .spot import SpotSerializer
from .fav import FavSerializer
from .comment import CommentSerializer
from .report import ReportSerializer
from .location import LocationSerializer
from plan.geo import convert_geo_to_location
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
        if len(res['spots']) > 0:
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

    def to_internal_value(self, data):
        res = {}
        fields = ('name', 'price', 'duration', 'note', 'spots')
        for key in fields:
            if key not in data:
                raise serializers.ValidationError({key: "This field is required."})
            res[key] = data[key]
        return res

    def create(self, validated_data):
        user = self.context['request'].user
        spots_data = validated_data.pop('spots')
        spot_count = len(spots_data)
        if spot_count < 2:
            raise serializers.ValidationError({"spots": "This fields must have more than 2."})
        lat, lon = 0, 0
        plan = Plan.objects.create(user=user, **validated_data)
        for spot_data in spots_data:
            Spot.objects.create(plan=plan, **spot_data)
            # 経度緯度を全て足し合わせる
            lat += spot_data['lat']
            lon += spot_data['lon']
        # spotの数で割った平均値でPlanのlocationを決める
        loc = convert_geo_to_location(lat / spot_count, lon / spot_count)
        plan.location = Location.objects.create(
            p_name=loc.p_name, p_code=loc.p_code, m_name=loc.m_name, m_code=loc.m_code
        )
        plan.save()
        return plan
