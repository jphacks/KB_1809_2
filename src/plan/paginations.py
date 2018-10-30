from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class UnwrapPagination(LimitOffsetPagination):
    """
    ページネーション結果をwrapせずにそのまま返す
    """

    def get_paginated_response(self, data):
        return Response(data)
