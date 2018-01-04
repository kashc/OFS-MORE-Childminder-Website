# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-04 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adults_In_Home',
            fields=[
                ('adult_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_names', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('birth_day', models.IntegerField(blank=True)),
                ('birth_month', models.IntegerField(blank=True)),
                ('birth_year', models.IntegerField(blank=True)),
                ('relationship', models.CharField(blank=True, max_length=100)),
                ('dbs_certificate_number', models.CharField(blank=True, max_length=50)),
                ('email', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'ADULT_IN_HOME',
            },
        ),
        migrations.CreateModel(
            name='Applicant_Home_Address',
            fields=[
                ('home_address_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('street_line1', models.CharField(blank=True, max_length=100)),
                ('street_line2', models.CharField(blank=True, max_length=100)),
                ('town', models.CharField(blank=True, max_length=100)),
                ('county', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('postcode', models.CharField(blank=True, max_length=8)),
                ('childcare_address', models.NullBooleanField()),
                ('move_in_month', models.IntegerField(blank=True)),
                ('move_in_year', models.IntegerField(blank=True)),
            ],
            options={
                'db_table': 'APPLICANT_HOME_ADDRESS',
            },
        ),
        migrations.CreateModel(
            name='Applicant_Names',
            fields=[
                ('name_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('current_name', models.BooleanField()),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_names', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'APPLICANT_NAME',
            },
        ),
        migrations.CreateModel(
            name='Applicant_Personal_Details',
            fields=[
                ('personal_detail_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('birth_day', models.IntegerField(blank=True, null=True)),
                ('birth_month', models.IntegerField(blank=True, null=True)),
                ('birth_year', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'APPLICANT_PERSONAL_DETAILS',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('application_type', models.CharField(blank=True, choices=[('CHILDMINDER', 'CHILDMINDER'), ('NANNY', 'NANNY'), ('NURSERY', 'NURSERY'), ('SOCIAL_CARE', 'SOCIAL_CARE')], max_length=50)),
                ('application_status', models.CharField(blank=True, choices=[('ARC_REVIEW', 'ARC_REVIEW'), ('CANCELLED', 'CANCELLED'), ('CYGNUM_REVIEW', 'CYGNUM_REVIEW'), ('DRAFTING', 'DRAFTING'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION'), ('NOT_REGISTERED', 'NOT_REGISTERED'), ('REGISTERED', 'REGISTERED'), ('REJECTED', 'REJECTED'), ('SUBMITTED', 'SUBMITTED'), ('WITHDRAWN', 'WITHDRAWN')], max_length=50)),
                ('cygnum_urn', models.CharField(blank=True, max_length=50)),
                ('login_details_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('personal_details_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('childcare_type_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('first_aid_training_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('eyfs_training_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('criminal_record_check_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('health_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('references_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('people_in_home_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('declarations_status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETE', 'COMPLETE'), ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')], max_length=50)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(blank=True, null=True)),
                ('date_accepted', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'APPLICATION',
            },
        ),
        migrations.CreateModel(
            name='Childcare_Type',
            fields=[
                ('childcare_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('zero_to_five', models.BooleanField()),
                ('five_to_eight', models.BooleanField()),
                ('eight_plus', models.BooleanField()),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
            ],
            options={
                'db_table': 'CHILDCARE_TYPE',
            },
        ),
        migrations.CreateModel(
            name='Children_In_Home',
            fields=[
                ('child_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_names', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('birth_day', models.IntegerField(blank=True)),
                ('birth_month', models.IntegerField(blank=True)),
                ('birth_year', models.IntegerField(blank=True)),
                ('relationship', models.CharField(blank=True, max_length=100)),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
            ],
            options={
                'db_table': 'CHILD_IN_HOME',
            },
        ),
        migrations.CreateModel(
            name='Criminal_Record_Check',
            fields=[
                ('criminal_record_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('dbs_certificate_number', models.CharField(blank=True, max_length=50)),
                ('cautions_convictions', models.BooleanField()),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
            ],
            options={
                'db_table': 'CRIMINAL_RECORD_CHECK',
            },
        ),
        migrations.CreateModel(
            name='First_Aid_Training',
            fields=[
                ('first_aid_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('training_organisation', models.CharField(max_length=100)),
                ('course_title', models.CharField(max_length=100)),
                ('course_day', models.IntegerField()),
                ('course_month', models.IntegerField()),
                ('course_year', models.IntegerField()),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
            ],
            options={
                'db_table': 'FIRST_AID_TRAINING',
            },
        ),
        migrations.CreateModel(
            name='Health_Declaration_Booklet',
            fields=[
                ('hdb_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('movement_problems', models.BooleanField()),
                ('breathing_problems', models.BooleanField()),
                ('heart_disease', models.BooleanField()),
                ('blackout_epilepsy', models.BooleanField()),
                ('mental_health_problems', models.BooleanField()),
                ('alcohol_drug_problems', models.BooleanField()),
                ('health_details', models.CharField(blank=True, max_length=500)),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
            ],
            options={
                'db_table': 'HEALTH_DECLARATION_BOOKLET',
            },
        ),
        migrations.CreateModel(
            name='Login_And_Contact_Details',
            fields=[
                ('login_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('mobile_number', models.CharField(blank=True, max_length=11)),
                ('add_phone_number', models.CharField(blank=True, max_length=11)),
                ('email_expiry_date', models.IntegerField(blank=True, null=True)),
                ('sms_expiry_date', models.IntegerField(blank=True, null=True)),
                ('magic_link_email', models.CharField(blank=True, max_length=100, null=True)),
                ('magic_link_sms', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'USER_DETAILS',
            },
        ),
        migrations.CreateModel(
            name='References',
            fields=[
                ('reference_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('relationship', models.CharField(blank=True, max_length=100)),
                ('years_known', models.IntegerField(blank=True)),
                ('months_known', models.IntegerField(blank=True)),
                ('street_line1', models.CharField(blank=True, max_length=100)),
                ('street_line2', models.CharField(blank=True, max_length=100)),
                ('town', models.CharField(blank=True, max_length=100)),
                ('county', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('postcode', models.CharField(blank=True, max_length=8)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('application_id', models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
            ],
            options={
                'db_table': 'REFERENCE',
            },
        ),
        migrations.AddField(
            model_name='application',
            name='login_id',
            field=models.ForeignKey(blank=True, db_column='login_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Login_And_Contact_Details'),
        ),
        migrations.AddField(
            model_name='applicant_personal_details',
            name='application_id',
            field=models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application'),
        ),
        migrations.AddField(
            model_name='applicant_names',
            name='personal_detail_id',
            field=models.ForeignKey(db_column='personal_detail_id', on_delete=django.db.models.deletion.CASCADE, to='application.Applicant_Personal_Details'),
        ),
        migrations.AddField(
            model_name='applicant_home_address',
            name='personal_detail_id',
            field=models.ForeignKey(db_column='personal_detail_id', on_delete=django.db.models.deletion.CASCADE, to='application.Applicant_Personal_Details'),
        ),
        migrations.AddField(
            model_name='adults_in_home',
            name='application_id',
            field=models.ForeignKey(db_column='application_id', on_delete=django.db.models.deletion.CASCADE, to='application.Application'),
        ),
    ]
