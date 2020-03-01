# Generated by Django 3.0.3 on 2020-02-07 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0001_initial'),
        ('Locations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patientID', models.CharField(max_length=35, primary_key=True, serialize=False, verbose_name='patientID')),
                ('studyID', models.CharField(max_length=35, unique=True, verbose_name='studyID')),
                ('date_of_birth', models.CharField(max_length=35)),
                ('prefix', models.CharField(blank=True, max_length=45, verbose_name='prefix')),
                ('firstName', models.CharField(max_length=45, verbose_name='firstName')),
                ('middleName', models.CharField(blank=True, max_length=45, verbose_name='middleName')),
                ('lastName', models.CharField(max_length=45, verbose_name='lastName')),
                ('suffix', models.CharField(blank=True, max_length=45, verbose_name='suffix')),
                ('com_name', models.CharField(blank=True, max_length=45, verbose_name='com_name')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, verbose_name='gender')),
                ('dur_hh', models.CharField(max_length=45, verbose_name='dur_hh')),
                ('exam_status', models.CharField(blank=True, max_length=30, verbose_name='exam_status')),
                ('notes', models.CharField(blank=True, max_length=500, verbose_name='notes')),
                ('lvl_edu', models.CharField(blank=True, max_length=45, verbose_name='lvl_edu')),
                ('work_status', models.CharField(blank=True, max_length=45, verbose_name='work_status')),
                ('marital_status', models.CharField(blank=True, max_length=45, verbose_name='marital_status')),
                ('motherFirstName', models.CharField(blank=True, max_length=45, verbose_name='motherFirstName')),
                ('motherLastName', models.CharField(blank=True, max_length=45, verbose_name='motherLastName')),
                ('tel1_num', models.CharField(blank=True, max_length=30, verbose_name='tel1_num')),
                ('tel1_owner', models.CharField(blank=True, max_length=45, verbose_name='tel1_owner')),
                ('tel1_owner_rel', models.CharField(blank=True, max_length=30, verbose_name='tel1_owner_relation')),
                ('tel2_num', models.CharField(blank=True, max_length=30, verbose_name='tel2_num')),
                ('tel2_owner', models.CharField(blank=True, max_length=45, verbose_name='tel2_owner')),
                ('tel2_owner_rel', models.CharField(blank=True, max_length=30, verbose_name='tel2_owner_relation')),
                ('nationalID', models.CharField(blank=True, max_length=30, verbose_name='nationalID')),
                ('deceased', models.IntegerField(choices=[(1, 'True'), (0, 'False')], default=0, verbose_name='deceased')),
                ('deceased_date', models.DateField(blank=True, default=None, null=True, verbose_name='deceased_date')),
                ('responder', models.CharField(max_length=30, verbose_name='responder')),
                ('proxy_name', models.CharField(blank=True, max_length=100, verbose_name='proxy_name')),
                ('proxy_rel', models.CharField(blank=True, max_length=100, verbose_name='proxy_rel')),
                ('enumeratorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Enumerator', verbose_name='EnumeratorID')),
                ('householdID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Locations.HouseHold', verbose_name='householdID')),
            ],
        ),
    ]
