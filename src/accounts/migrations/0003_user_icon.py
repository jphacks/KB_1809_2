# Generated by Django 2.1.2 on 2018-10-20 07:05

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181020_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, default='/media/icon/user.png', null=True, upload_to=accounts.models.get_image_path, verbose_name='アイコン'),
        ),
    ]
