# Generated by Django 2.1.2 on 2018-10-28 06:27

from django.db import migrations
import imagekit.models.fields
import plan.models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0010_auto_20181028_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to=plan.models.get_image_path, verbose_name='投稿画像'),
        ),
    ]
