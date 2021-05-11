# Generated by Django 3.2 on 2021-04-27 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('data_access_of_all_countries', models.TextField(blank=True, null=True)),
                ('one_year_validity', models.CharField(blank=True, max_length=255, null=True)),
                ('unlimited_full_shipment_view', models.CharField(blank=True, max_length=255, null=True)),
                ('unlimited_importer_exporter_view', models.CharField(blank=True, max_length=255, null=True)),
                ('unlimited_view_of_linkedin_contacts', models.CharField(blank=True, max_length=255, null=True)),
                ('unlimited_view_charts_and_dashboard', models.CharField(blank=True, max_length=255, null=True)),
                ('unlimited_searches', models.IntegerField(blank=True, null=True)),
                ('number_of_workspaces', models.IntegerField(blank=True, null=True)),
                ('workspace_deletion', models.IntegerField(blank=True, null=True)),
                ('workspace_shipment_limit', models.BigIntegerField(blank=True, null=True)),
                ('shipment_credits_for_excel_download', models.BigIntegerField(blank=True, null=True)),
                ('roll_over_points_to_next_year', models.CharField(blank=True, max_length=255, null=True)),
                ('download_buyers_or_suppliers_contact_profile', models.IntegerField(blank=True, null=True)),
                ('contact_details_phone_and_email', models.IntegerField(blank=True, null=True)),
                ('hot_products', models.IntegerField(blank=True, null=True)),
                ('hot_companies', models.CharField(blank=True, max_length=255, null=True)),
                ('users_count', models.IntegerField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Plans_created_by', to=settings.AUTH_USER_MODEL)),
                ('owned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Plans_owned_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Plans_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Plans',
            },
        ),
    ]