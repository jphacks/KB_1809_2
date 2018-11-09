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
    Planを都道府県名や市区町村名，スポット名でフィルタする (or)
    """
    location = filters.CharFilter(method='filter_words')

    class Meta:
        models = models.Plan
        fields = ('location',)

    def filter_words(self, queryset, name, value):
        if self.request.version == "v1":
            return queryset.filter(
                Q(location__p_name__contains=value) | Q(location__m_name__contains=value)
            )

        querys = list()
        for word in value.split(" "):
            querys.append(Q(location__p_name__contains=word))
            querys.append(Q(location__m_name__contains=word))
            querys.append(Q(name__contains=word))
            querys.append(Q(spots__name__contains=word))
        query = querys.pop()
        for q in querys:
            query |= q
        return queryset.filter(query).distinct()


