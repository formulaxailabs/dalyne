# Generated by Django 3.2 on 2021-04-30 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0006_auto_20210430_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importtable',
            name='IMPORTER_CITY_STATE',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='importtable',
            name='IMPORTER_EMAIL',
            field=models.TextField(blank=True, null=True),
        ),
    ]