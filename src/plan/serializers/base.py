from rest_framework import serializers


class BaseListSerializer(serializers.ListSerializer):
    """
    基底となるListSerializer
    """

    def update(self, instance, validated_data):
        instance_mapping = {i.id: i for i in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for instance_id, given_data in data_mapping.items():
            instance_obj = instance_mapping.get(instance_id)
            if instance_obj:
                # 既に存在するIDなので情報をアップデート
                ret.append(self.child.update(instance_obj, given_data))
            else:
                # 存在しないので作成
                ret.append(self.child.create(given_data))
        for instance_id, instance_obj in instance_mapping.items():
            if instance_id not in data_mapping:
                # DBに存在するがPOSTされてきたデータに存在しないデータを削除
                instance_obj.delete()
        return ret
