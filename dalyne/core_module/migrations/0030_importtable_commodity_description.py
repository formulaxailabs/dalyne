# Generated by Django 3.2 on 2021-06-10 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0029_alter_productmaster_hs_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='importtable',
            name='commodity_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
