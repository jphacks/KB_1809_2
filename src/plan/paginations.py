from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class VersioningPagination(LimitOffsetPagination):
    """
    api/v1/ならページネーションしない．v2ならページネーションする．
    """

    def get_paginated_response(self, data):
        return Response(data)
