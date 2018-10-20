import os
import uuid
from django.db import models
from django.conf import settings


def get_image_path(instance, filename):
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return name + extension


class Location(models.Model):
    """
    地点データ
    """
    p_name = models.CharField("都道府県名", max_length=255)
    p_code = models.IntegerField("都道府県コード")
    m_name = models.CharField("市区町村名", max_length=255)
    m_code = models.IntegerField("市区町村コード")


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
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="plans", verbose_name="位置情報",
                                 null=True, blank=True)
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)


class Spot(models.Model):
    """
    店や場所など点のデータ
    """
    name = models.CharField("スポット名", max_length=255, default="")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="spots", verbose_name="プラン")
    lat = models.FloatField("緯度")
    lon = models.FloatField("経度")
    note = models.TextField("ノート")
    image = models.ImageField("投稿画像", upload_to=get_image_path)
    order = models.IntegerField("回る順番", default=0)
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    class Meta:
        unique_together = ("plan", "order")


class Fav(models.Model):
    """
    ユーザーがお気に入りしたPlanのデータ
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favs",
                             verbose_name="ユーザー")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="favs", verbose_name="プラン")
    created_at = models.DateTimeField("お気に入りした日時", auto_now_add=True)


class Comment(models.Model):
    """
    ユーザーがプランに対して送ったコメントのデータ
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments",
                             verbose_name="ユーザー")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="comments", verbose_name="プラン")
    text = models.TextField("テキスト")
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)


class Report(models.Model):
    """
    プランを参考にしてデートしたユーザーのレポートのデータ
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports",
                             verbose_name="ユーザー")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="reports", verbose_name="プラン")
    text = models.TextField("テキスト")
    image = models.ImageField("投稿画像", upload_to=get_image_path)
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)
