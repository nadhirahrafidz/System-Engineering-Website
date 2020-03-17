from django.db import models
from Locations.models import HouseHold
from Users.models import Enumerator


class Patient(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    BOOLEAN = (
        (1, 'True'),
        (0, 'False'),
    )
    patientID = models.CharField(verbose_name='patientID', max_length=35, primary_key=True)
    studyID = models.CharField(verbose_name='studyID', max_length=35, unique=True)
    date_of_birth = models.CharField(verbose_name='date_of_birth', max_length=35)
    prefix = models.CharField(verbose_name='prefix', max_length=45, blank=True)
    firstName = models.CharField(verbose_name='firstName', max_length=45)
    middleName = models.CharField(verbose_name='middleName', max_length=45, blank=True)
    lastName = models.CharField(verbose_name='lastName', max_length=45)
    suffix = models.CharField(verbose_name='suffix', blank=True, max_length=45)
    com_name = models.CharField(verbose_name='com_name', blank=True, max_length=45)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER)
    householdID = models.ForeignKey(HouseHold, verbose_name='householdID', on_delete=models.CASCADE)
    dur_hh = models.CharField(verbose_name='dur_hh', max_length=45)
    notes = models.CharField(verbose_name='notes', blank=True, max_length=500)
    lvl_edu = models.CharField(verbose_name='lvl_edu', max_length=45, blank=True)
    work_status = models.CharField(verbose_name='work_status', max_length=45, blank=True)
    marital_status = models.CharField(verbose_name='marital_status', max_length=45, blank=True)
    motherFirstName = models.CharField(verbose_name='motherFirstName', max_length=45, blank=True)
    motherLastName = models.CharField(verbose_name='motherLastName', max_length=45, blank=True)
    tel1_num = models.CharField(verbose_name='tel1_num', max_length=30, blank=True)
    tel1_owner = models.CharField(verbose_name='tel1_owner', max_length=45, blank=True)
    tel1_owner_rel = models.CharField(verbose_name='tel1_owner_relation', max_length=30, blank=True)
    tel2_num = models.CharField(verbose_name='tel2_num', max_length=30, blank=True)
    tel2_owner = models.CharField(verbose_name='tel2_owner', max_length=45, blank=True)
    tel2_owner_rel = models.CharField(verbose_name='tel2_owner_relation', max_length=30, blank=True)
    enumeratorID = models.ForeignKey(Enumerator, verbose_name='EnumeratorID', on_delete=models.CASCADE)
    nationalID = models.CharField(verbose_name='nationalID', max_length=30, blank=True)
    deceased = models.IntegerField(verbose_name='deceased', default=0, choices=BOOLEAN)
    deceased_date = models.CharField(verbose_name='deceased_date', blank=True, null=True, max_length=30)
    responder = models.CharField(verbose_name='responder', max_length=30)
    proxy_name = models.CharField(verbose_name='proxy_name', max_length=100, blank=True)
    proxy_rel = models.CharField(verbose_name='proxy_rel', max_length=100, blank=True)

