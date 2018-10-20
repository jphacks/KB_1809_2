# Generated by Django 2.1.2 on 2018-10-20 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_auto_20181020_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='スポット名'),
        ),
        migrations.AddField(
            model_name='spot',
            name='order',
            field=models.IntegerField(default=0, verbose_name='回る順番'),
        ),
        migrations.AlterUniqueTogether(
            name='spot',
            unique_together={('plan', 'order')},
        ),
    ]