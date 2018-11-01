import os
import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


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

    class Meta:
        ordering = ('p_code', 'm_code')
        unique_together = ('p_name', 'p_code', 'm_name', 'm_code')

    def __str__(self):
        """都道府県名+市区町村名を返却"""
        return self.p_name + " " + self.m_name


class Plan(models.Model):
    """
    全体の工程を示すPlanのモデル
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='plans', verbose_name='ユーザ')
    name = models.CharField("コース名", max_length=255)
    price = models.IntegerField("予算", default=0)
    duration = models.IntegerField("かかる時間", default=0)
    note = models.TextField("投稿内容")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="plans", verbose_name="位置情報",
                                 null=True, blank=True)
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    class Meta:
        ordering = ('-created_at', 'name')

    def __str__(self):
        """プランの名前を返却"""
        return self.name

    def favorite_count(self):
        """お気に入りされた数を返す"""
        return self.favs.count()

    def comment_count(self):
        """コメントの数を返す"""
        return self.comments.count()


class Spot(models.Model):
    """
    店や場所など点のデータ
    """
    name = models.CharField("スポット名", max_length=255, default="")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="spots", verbose_name="プラン",
                             null=True, blank=True)
    lat = models.FloatField("緯度")
    lon = models.FloatField("経度")
    note = models.TextField("ノート")
    image = ProcessedImageField(verbose_name="投稿画像",
                                upload_to=get_image_path,
                                processors=[ResizeToFit(*settings.PLANNAP_IMAGE_SIZES['SPOT'])],
                                format='JPEG',
                                options={'quality': 80})
    order = models.IntegerField("回る順番", default=0)
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    def __str__(self):
        """スポット名を返却"""
        return self.name

    class Meta:
        ordering = ('order',)
        unique_together = ("plan", "order")


class Fav(models.Model):
    """
    ユーザーがお気に入りしたPlanのデータ
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favs",
                             verbose_name="ユーザー")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="favs", verbose_name="プラン")
    created_at = models.DateTimeField("お気に入りした日時", auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('user', 'plan')

    def __str__(self):
        return str(self.user) + ' favorited ' + str(self.plan)


class Comment(models.Model):
    """
    ユーザーがプランに対して送ったコメントのデータ
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments",
                             verbose_name="ユーザー")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="comments", verbose_name="プラン")
    text = models.TextField("テキスト")
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.user) + ' commented on ' + str(self.plan)


class Report(models.Model):
    """
    プランを参考にしてデートしたユーザーのレポートのデータ
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports",
                             verbose_name="ユーザー")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="reports", verbose_name="プラン")
    text = models.TextField("テキスト")
    image = ProcessedImageField(verbose_name="投稿画像",
                                upload_to=get_image_path,
                                processors=[ResizeToFit(*settings.PLANNAP_IMAGE_SIZES['REPORT'])],
                                format='JPEG',
                                options={'quality': 80})
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user) + ' reported about' + str(self.plan)


@receiver(models.signals.post_delete, sender=Spot)
@receiver(models.signals.post_delete, sender=Report)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    レコード削除時にファイルも削除する
    """
    if instance.image:
        img = instance.image.path
        if os.path.isfile(img):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Spot)
@receiver(models.signals.pre_save, sender=Report)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    レコードの更新時にファイルの変更があれば古いものを削除する
    """
    # PrimaryKeyを持たない（=更新では無く作成の）場合
    if not instance.pk:
        return None

    try:
        old_image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return None

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
