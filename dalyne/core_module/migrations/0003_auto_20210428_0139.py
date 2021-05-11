# Generated by Django 3.2 on 2021-04-27 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0002_plans'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='validity_of_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core_module.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserPlans_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserPlans_owned_by', to=settings.AUTH_USER_MODEL)),
                ('plans', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core_module.plans')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserPlans_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserPlans',
            },
        ),
    ]