# Generated by Django 3.2 on 2021-05-18 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_module', '0013_auto_20210518_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plans',
            old_name='contact_details_phone_and_email',
            new_name='download_points',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='download_buyers_or_suppliers_contact_profile',
            new_name='hot_company',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='number_of_workspaces',
            new_name='pakage_validity',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='hot_companies',
            new_name='searches',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='unlimited_searches',
            new_name='shipment_limit_in_workspaces',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='users_count',
            new_name='unlimited_data_access',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='validity_of_days',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='plans',
            old_name='workspace_deletion',
            new_name='workspaces',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='data_access_of_all_countries',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='one_year_validity',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='roll_over_points_to_next_year',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='shipment_credits_for_excel_download',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='unlimited_full_shipment_view',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='unlimited_importer_exporter_view',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='unlimited_view_charts_and_dashboard',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='unlimited_view_of_linkedin_contacts',
        ),
        migrations.RemoveField(
            model_name='plans',
            name='workspace_shipment_limit',
        ),
        migrations.AddField(
            model_name='plans',
            name='add_on_points_Facility',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plans',
            name='hot_company_postfix',
            field=models.CharField(choices=[('Per Qtr', 'Per Qtr'), ('Per year', 'Per year')], default='Per Qtr', max_length=50),
        ),
        migrations.AddField(
            model_name='plans',
            name='hot_products_postfix',
            field=models.CharField(choices=[('Per Qtr', 'Per Qtr'), ('Per year', 'Per year')], default='Per Qtr', max_length=50),
        ),
        migrations.AddField(
            model_name='plans',
            name='pakage_postfix',
            field=models.CharField(choices=[('days', 'days'), ('months', 'months'), ('year', 'year'), ('quaterly', 'quaterly')], default='months', max_length=50),
        ),
        migrations.AddField(
            model_name='plans',
            name='unlimited_data_access_postfix',
            field=models.CharField(choices=[('days', 'days'), ('months', 'months'), ('year', 'year'), ('quaterly', 'quaterly')], default='months', max_length=50),
        ),
        migrations.AddField(
            model_name='plans',
            name='workspaces_deletion_per_qtr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plans',
            name='workspaces_validity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plans',
            name='workspaces_validity_postfix',
            field=models.CharField(choices=[('days', 'days'), ('months', 'months'), ('year', 'year'), ('quaterly', 'quaterly')], default='months', max_length=50),
        ),
    ]
