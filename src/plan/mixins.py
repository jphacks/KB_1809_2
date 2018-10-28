from rest_framework.response import Response


class NestedListMixin(object):
    """
    /plans/<plan_pk>/favs/ のようなネストされた要素に対してリストを返す時のmixin
    """
    def _serialize(self, serializer_class, queryset, *args, **kwargs):
        """
        Serializerの指定があればそれで返す．無ければself.get_serializerする．
        :param serializer_class: 使用するSerializerクラスを指定する
        :param args: Serializerをインスタンス化する際の位置引数
        :param kwargs: Serializerをインスタンス化する際のオプション引数
        :return: インスタンス化されたSerializer
        """
        if serializer_class is None:
            if 'context' in kwargs.keys():
                kwargs.pop('context')
            return self.get_serializer(queryset, *args, **kwargs)
        return serializer_class(queryset, *args, context=self.get_serializer_context(), **kwargs)

    def list(self, request, plan_pk=None, serializer_class=None, **kwargs):
        """
        plan_pkでフィルタリングしてレスポンスを返す
        :param request: ユーザのリクエストオブジェクト
        :param plan_pk: フィルタ対象のPlanのPrimary Key
        :param serializer_class: 使用するSerializer．デフォルトはself.serializerになる．
        :param kwargs: その他オプション
        :return:
        """
        if plan_pk is None:
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(plan_id=plan_pk).all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self._serialize(serializer_class, page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self._serialize(queryset, page, many=True)
        return Response(serializer.data)
