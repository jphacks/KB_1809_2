from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from . import models, serializers, permissions


class LocationFilter(filters.FilterSet):
    # フィルタの定義
    p_name = filters.CharFilter(lookup_expr="contains")
    m_name = filters.CharFilter(lookup_expr="contains")

    class Meta:
        model = models.Location
        fields = ['p_name', 'm_name']


class LocationViewSets(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.LocationSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = LocationFilter


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


class FavViewSets(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = models.Fav.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.FavSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)

    def list(self, request, plan_pk=None, **kwargs):
        if not plan_pk:
            return super(FavViewSets, self).list(request, **kwargs)
        user = request.user
        favs = self.queryset.filter(plan_id=plan_pk, user=user).all()
        serializer = self.get_serializer(favs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, plan_pk=None, **kwargs):
        if not plan_pk:
            return super(FavViewSets, self).retrieve(request, pk, **kwargs)
        fav = get_object_or_404(self.queryset, pk=pk, plan_id=plan_pk)
        serializer = self.get_serializer(fav)
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=False, url_path='me')
    def me(self, request, plan_pk=None, **kwargs):
        if request.method == 'POST':
            return self.create(request, plan_pk=plan_pk, **kwargs)
        try:
            fav = self.queryset.filter(plan_id=plan_pk, user=request.user).get()
        except models.Fav.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fav.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, plan_pk=None, **kwargs):
        if not plan_pk:
            return super(FavViewSets, self).create(request, **kwargs)
        serializer = self.get_serializer(data={'plan_id': plan_pk})
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSets(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)


class PlanLocationFilter(filters.FilterSet):
    location = filters.CharFilter(method='filter_p_and_m_name')

    class Meta:
        models = models.Plan
        fields = ('location',)

    def filter_p_and_m_name(self, queryset, name, value):
        return queryset.filter(
            Q(location__p_name__contains=value)| Q(location__m_name__contains=value)
        )


class PlanViewSets(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.PlanSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)
    filter_class = PlanLocationFilter

    def list(self, request, *args, **kwargs):
        """一覧表示の場合は情報を削減したSerializerを使用する"""
        serializer = serializers.AbstractPlanSerializer(self.filter_queryset(models.Plan.objects.all()),
                                                        many=True, context={'request': request})
        return Response(serializer.data)

