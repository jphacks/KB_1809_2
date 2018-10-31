from base64 import b64encode
from urllib import parse as urlparse
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, CursorPagination


class UnwrapPagination(PageNumberPagination):
    """
    ページネーション結果をwrapせずにそのまま返す
    """

    def get_paginated_response(self, data):
        return Response(data)


class TimestampCursorPagination(CursorPagination):
    """
    時系列で要素が重複しないようにタイムスタンプを使ってページネーションする
    """
    ordering = '-created_at'
    page_size = 5

    def paginate_queryset(self, queryset, request, view=None):
        page = super(TimestampCursorPagination, self).paginate_queryset(queryset, request, view)
        # get_paginated_responseでrequestのバージョンから判定するためにここでインスタンス変数に代入しておく
        self.request = request
        return page

    def encode_cursor(self, cursor):
        """
        元のメソッドをオーバーライドしてcursorクエリだけを返す
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position
        querystring = urlparse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded

    def get_paginated_response(self, data):
        if self.request.version == 'v1':
            return Response(data)
        return super(TimestampCursorPagination, self).get_paginated_response(data)
