# Generated by Django 3.2 on 2021-05-21 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0023_filterdatamodel_total_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterdatamodel',
            name='workspace_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
