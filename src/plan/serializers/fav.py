from rest_framework import serializers

from plan.models import Fav, Plan
from accounts.models import User

from accounts.serializers import SimpleUserSerializer


class FavListSerializer(serializers.ListSerializer):
    """
    複数のFavを処理するSerializer
    """

    def create(self, validated_data):
        favs = [Fav(**item) for item in validated_data]
        return Fav.objects.bulk_create(favs)

    def update(self, instance, validated_data):
        fav_mapping = {fav.id: fav for fav in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for fav_id, spot_data in data_mapping.items():
            fav = fav_mapping.get(fav_id)
            if fav:
                # 既に存在するIDなので情報をアップデート
                ret.append(self.child.update(fav, spot_data))
            else:
                # 存在しないので作成
                ret.append(self.child.create(spot_data))
        for fav_id, fav in fav_mapping.items():
            if fav_id not in data_mapping:
                # DBに存在するがPOSTされてきたデータに存在しないデータを削除
                fav.delete()
        return ret


class FavSerializer(serializers.ModelSerializer):
    """
    単一のFavを処理するSerializer
    """

    user = SimpleUserSerializer()
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = Fav
        fields = ("pk", "user", "plan")
        list_serializer_class = FavListSerializer

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
