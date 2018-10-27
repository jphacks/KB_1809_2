from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class VersioningPagination(LimitOffsetPagination):
    """
    api/v1/ならページネーションしない．v2ならページネーションする．
    """

    def get_paginated_response(self, data):
        if self.request.version == 'v1':
            return Response(data)
        return super(VersioningPagination, self).get_paginated_response(data)
