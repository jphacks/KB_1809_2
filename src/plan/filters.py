from django.db.models import Q
from django_filters import rest_framework as filters
from . import models


class LocationFilter(filters.FilterSet):
    """
    都道府県名や市区町村名でフィルタする (and)
    """
    # フィルタの定義
    p_name = filters.CharFilter(lookup_expr="contains")
    m_name = filters.CharFilter(lookup_expr="contains")

    class Meta:
        model = models.Location
        fields = ['p_name', 'm_name']


class PlanLocationFilter(filters.FilterSet):
    """
    Planを都道府県名や市区町村名でフィルタする (or)
    """
    location = filters.CharFilter(method='filter_p_and_m_name')

    class Meta:
        models = models.Plan
        fields = ('location',)

    def filter_p_and_m_name(self, queryset, name, value):
        return queryset.filter(
            Q(location__p_name__contains=value) | Q(location__m_name__contains=value)
        )


