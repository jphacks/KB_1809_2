from rest_framework import serializers

from plan.models import Plan, Spot
from .spot import SpotSerializer
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
                  'created_at', 'user', 'favorite_count', 'comment_count', 'map_url')
        extra_kwargs = {
            'map_url': {'read_only': True},
            'favorite_count': {'read_only': True},
            'comment_count': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super(AbstractPlanSerializer, self).to_representation(instance)
        all_spots = data['spots']
        if len(data['spots']) > 0:
            data['spots'] = [all_spots[0], all_spots[-1]]
        data['is_favorite'] = instance.favs.filter(user=self.context['request'].user).exists()
        if self.context['request'].version == 'v2':
            data['created_at'] = int(instance.created_at.strftime('%s'))
        return data


class PlanSerializer(serializers.ModelSerializer):
    """
    単一のPlanの処理
    """

    spots = SpotSerializer(many=True, allow_null=True)
    reports = ReportSerializer(many=True, allow_null=True, read_only=True)
    user = SimpleUserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Plan
        fields = ('pk', 'name', 'price', 'duration', 'note', 'location',
                  'reports', 'created_at', 'spots', 'user', 'map_url',
                  'favorite_count', 'comment_count')
        extra_kwargs = {
            'map_url': {'read_only': True},
            'favorite_count': {'read_only': True},
            'comment_count': {'read_only': True},
        }

    def to_internal_value(self, data):
        # res = {}
        # spotの数で割った平均値でPlanのlocationを決める
        spots_count = len(data['spots'])
        if spots_count < 2:
            raise serializers.ValidationError({'spots': 'This field must have more than two spots.'})
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

    def update(self, instance, validated_data):
        # spot
        Spot.objects.filter(plan_id=instance.pk).delete()
        spots = validated_data['spots']
        self.get_or_create_spots(spots, instance.pk)

        # location
        instance.location = self.get_or_create_location(spots)

        # other
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.duration = validated_data['duration']
        instance.note = validated_data['note']

        instance.save()
        return instance

    def create(self, validated_data):
        user = self.context['request'].user
        spots_data = validated_data.pop('spots')

        # Planを作成してidを入手
        plan = Plan.objects.create(user=user, **validated_data)
        self.get_or_create_spots(spots_data, plan.pk)

        # 位置情報を地域名に変換
        plan.location = self.get_or_create_location(spots_data)

        plan.save()
        return plan

    @staticmethod
    def get_or_create_spots(spots, plan_id):
        """
        指定のPlan IDに紐づくSpotを作成する
        :param spots: JSON Spot list
        :param plan_id: Plan`s primary key
        :return: None
        """
        for i in range(len(spots)):
            spots[i]['plan_id'] = plan_id
        ss = SpotSerializer(data=spots, many=True)
        ss.is_valid(raise_exception=True)
        ss.save()

    @staticmethod
    def get_or_create_location(spots):
        """
        SpotからPlanの座標を計算してLocationを作成する
        :param spots: JSON Spot List
        :return: Location model object
        """
        n_spots = len(spots)
        lat = sum([s['lat'] for s in spots]) / n_spots
        lon = sum([s['lon'] for s in spots]) / n_spots
        loc = convert_geo_to_location(lat, lon)
        location_serializer = LocationSerializer(data=loc.__dict__)
        location_serializer.is_valid(raise_exception=True)
        return location_serializer.save()

    def to_representation(self, instance):
        data = super(PlanSerializer, self).to_representation(instance)
        data['is_favorite'] = instance.favs.filter(user=self.context['request'].user).exists()
        if self.context['request'].version == 'v2':
            data['created_at'] = int(instance.created_at.strftime('%s'))
        return data
