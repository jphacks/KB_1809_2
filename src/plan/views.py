from rest_framework import viewsets, status, mixins, generics
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import (
    filters,
    models,
    serializers,
    permissions,
    paginations,
    mixins as custom_mixins,
)


class LocationViewSets(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Locationの詳細を取得

    list:
    Locationの一覧を取得
    """
    queryset = models.Location.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.LocationSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = filters.LocationFilter
    pagination_class = paginations.UnwrapPagination


class SpotViewSets(viewsets.ModelViewSet):
    queryset = models.Spot.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.SpotSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)


class ReportViewSets(viewsets.ModelViewSet):
    queryset = models.Report.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.ReportSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)


class FavViewSets(custom_mixins.PlanNestedListMixin,
                  custom_mixins.PlanNestedDestroyMixin,
                  custom_mixins.PlanNestedRetrieveMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    ふぁぼのエンドポイント

    retrieve:
        ふぁぼの詳細を取得

    list:
        指定したPlanのふぁぼ一覧を取得

    create:
        指定したPlanをふぁぼする

    destroy:
        指定したPlanのふぁぼを解除する
    """
    queryset = models.Fav.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.FavSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)

    @action(methods=['post', 'delete'], detail=False, url_path='me')
    def me(self, request, plan_pk=None, **kwargs):
        """POSTでふぁぼ，DELETEであんふぁぼする"""
        if request.method == 'POST':
            return self.create(request, plan_pk=plan_pk, **kwargs)
        try:
            fav = self.queryset.filter(plan_id=plan_pk, user=request.user).get()
        except models.Fav.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fav.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, plan_pk=None, **kwargs):
        serializer = self.get_serializer(data={'plan_id': int(plan_pk)})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSets(custom_mixins.PlanNestedListMixin,
                      custom_mixins.PlanNestedDestroyMixin,
                      custom_mixins.PlanNestedRetrieveMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """
    retrieve:
        コメントの詳細を取得する

    list:
        特定のPlanに紐付くコメントの一覧を取得する

    create:
        特定のPlanに対してコメントを投稿する

    destroy:
        指定したコメントを削除する
    """
    queryset = models.Comment.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)

    def create(self, request, plan_pk=None, **kwargs):
        data = request.data
        data['plan_id'] = int(plan_pk)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PlanViewSets(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   custom_mixins.PlanNestedListMixin,
                   viewsets.GenericViewSet):
    """
    retrieve:
        Planの詳細を取得する

    create:
        Planを作成する．`spots`で指定した複数のSpotの緯度経度からそのPlanの緯度経度を推定する．

    list:
        Planの一覧を表示する．情報を削減したSerializerを用い，commentsやreportsなどは返さない．

    destroy:
        Planを削除する
    """
    queryset = models.Plan.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.PlanSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)
    filter_class = filters.PlanLocationFilter

    def list(self, request, *args, **kwargs):
        return super(PlanViewSets, self).list(
            request, serializer_class=serializers.AbstractPlanSerializer, *args, **kwargs
        )


class MyFavPlanView(generics.ListAPIView):
    """
    自身がふぁぼしたPlanに関するエンドポイント

    list:
        ふぁぼったPlan一覧を返すエンドポイント
    """
    queryset = models.Plan.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.PlanSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(favs__user=self.request.user).all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserPlanView(custom_mixins.UserNestedListMixin,
                   viewsets.GenericViewSet):
    """
    指定したユーザのPlanについてのエンドポイント．

    list:
        指定したユーザが投稿したPlan一覧を返すエンドポイント
    """
    queryset = models.Plan.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.AbstractPlanSerializer
    permission_classes = (IsAuthenticated,)
