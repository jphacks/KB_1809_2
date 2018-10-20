from django.db import models
from django.conf import settings


class Plan(models.Model):
    """
    全体の工程を示すPlanのモデル
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='plans', verbose_name='ユーザ')
    name = models.CharField("コース名", max_length=255)
    price = models.IntegerField("予算", default=0)
    duration = models.IntegerField("かかる時間", default=0)
    lat = models.FloatField("緯度")
    lon = models.FloatField("経度")
    note = models.TextField("投稿内容")
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)


class Location(models.Model):
    """
    地点データ
    """
    p_name = models.CharField("都道府県名", max_length=255)
    p_code = models.IntegerField("都道府県コード")
    m_name = models.CharField("市区町村名", max_length=255)
    m_code = models.IntegerField("市区町村コード")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="location", verbose_name="プラン")


class Spot(models.Model):
    """
    店や場所など点のデータ
    """
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="spots", verbose_name="プラン")
    lat = models.FloatField("緯度")
    lon = models.FloatField("経度")
    note = models.TextField("ノート")
    image = models.ImageField("投稿画像")
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)
