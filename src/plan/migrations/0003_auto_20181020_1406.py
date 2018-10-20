# Generated by Django 2.1.2 on 2018-10-20 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_plan_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='plan',
        ),
        migrations.AddField(
            model_name='plan',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='plan.Location', verbose_name='位置情報'),
        ),
    ]
