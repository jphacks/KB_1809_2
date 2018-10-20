from rest_framework import viewsets
from rest_framework.parsers import JSONParser


from . import models, serializers


class LocationViewSets(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.LocationSerializer


class SpotViewSets(viewsets.ModelViewSet):
    queryset = models.Spot.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.SpotSerializer


class ReportViewSets(viewsets.ModelViewSet):
    queryset = models.Report.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.ReportSerializer


class FavViewSets(viewsets.ModelViewSet):
    queryset = models.Fav.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.FavSerializer


class CommentViewSets(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.CommentSerializer
