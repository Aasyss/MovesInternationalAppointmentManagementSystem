# Generated by Django 4.2.4 on 2023-09-13 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setup_availability',
            old_name='friday_endtime',
            new_name='friday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='friday_starttime',
            new_name='friday_start_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='monday_endtime',
            new_name='monday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='monday_starttime',
            new_name='monday_start_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='saturday_endtime',
            new_name='saturday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='saturday_starttime',
            new_name='saturday_start_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='startdate',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='sunday_endtime',
            new_name='sunday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='sunday_starttime',
            new_name='sunday_start_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='thursday_endtime',
            new_name='thursday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='thursday_starttime',
            new_name='thursday_start_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='tuesday_endtime',
            new_name='tuesday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='tuesday_starttime',
            new_name='tuesday_start_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='wednesday_endtime',
            new_name='wednesday_end_time',
        ),
        migrations.RenameField(
            model_name='setup_availability',
            old_name='wednesday_starttime',
            new_name='wednesday_start_time',
        ),
    ]
