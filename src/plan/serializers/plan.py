from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from plan.models import Spot


class SpotListSerializer(serializers.ListSerializer):
    """
    Spotを複数処理するserializer
    """

    def create(self, validated_data):
        spots = [Spot(**item) for item in validated_data]
        return Spot.objects.bulk_create(spots)

    def update(self, instance, validated_data):
        # それぞれidとその中身のリストにする
        spot_mapping = {sp.id: sp for sp in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for spot_id, spot_data in data_mapping.items():
            spot = spot_mapping.get(spot_id)
            if spot:
                # 既に存在するIDなので情報をアップデート
                ret.append(self.child.update(spot, spot_data))
            else:
                # 存在しないので作成
                ret.append(self.child.create(spot_data))
        for spot_id, spot in spot_mapping.items():
            if spot_id not in data_mapping:
                # DBに存在するがPOSTされてきたデータに存在しないデータを削除
                spot.delete()

        return ret


class SpotSerializer(serializers.ModelSerializer):

    """
    単一のSpotを処理するSerializer
    """

    image = Base64ImageField()

    class Meta:
        model = Spot
        fields = ("pk", "name", "order", "lat", "lon", "note", "image", "created_at")
