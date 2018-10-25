from rest_framework import serializers

from plan.models import Plan
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
        res['is_favorite'] = instance.favs.filter(user=self.context['request'].user).exists()
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
        # res = {}
        # spotの数で割った平均値でPlanのlocationを決める
        spots_count = len(data['spots'])
        if spots_count < 2:
            raise serializers.ValidationError({'spots': 'This field must have more than two spots.'})
        data['lat'] = sum([d['lat'] for d in data['spots']]) / spots_count
        data['lon'] = sum([d['lon'] for d in data['spots']]) / spots_count
        return data

    def validate(self, attrs):
        """必須フィールドを含んでいるかのバリデーション"""
        fields = ('name', 'price', 'duration', 'note', 'spots')
        for key in fields:
            if key not in attrs:
                raise serializers.ValidationError({key: "This field is required."})
        return attrs

    def validate_spots(self, spots):
        """spotsが2つ以上含まれているかのバリデーション"""
        if len(spots) < 2:
            raise serializers.ValidationError('This field must have more than two spots.')
        return spots

    def create(self, validated_data):
        user = self.context['request'].user
        spots_data = validated_data.pop('spots')
        lat = validated_data.pop('lat')
        lon = validated_data.pop('lon')
        # Planを作成してidを入手
        plan = Plan.objects.create(user=user, **validated_data)
        for i in range(len(spots_data)):
            spots_data[i]['plan_id'] = plan.pk
        ss = SpotSerializer(data=spots_data, many=True)
        ss.is_valid(raise_exception=True)
        ss.save()
        # 位置情報を地域名に変換
        loc = convert_geo_to_location(lat, lon)
        location_serializer = LocationSerializer(data=loc.__dict__)
        location_serializer.is_valid(raise_exception=True)
        plan.location = location_serializer.save()
        plan.save()
        return plan

    def to_representation(self, instance):
        data = super(PlanSerializer, self).to_representation(instance)
        data['is_favorite'] = instance.favs.filter(user=self.context['request'].user).exists()
        return data
