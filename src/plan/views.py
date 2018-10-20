from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated


from . import models, serializers


class LocationViewSets(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.LocationSerializer
    permission_classes = (IsAuthenticated,)


class SpotViewSets(viewsets.ModelViewSet):
    queryset = models.Spot.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.SpotSerializer
    permission_classes = (IsAuthenticated,)


class ReportViewSets(viewsets.ModelViewSet):
    queryset = models.Report.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.ReportSerializer
    permission_classes = (IsAuthenticated,)


class FavViewSets(viewsets.ModelViewSet):
    queryset = models.Fav.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.FavSerializer
    permission_classes = (IsAuthenticated,)


class CommentViewSets(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated,)
