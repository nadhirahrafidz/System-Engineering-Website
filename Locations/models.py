from django.db import models
from Users.models import Enumerator

class Location(models.Model):
    # AutoField is an Integer field that auto-increments
    locationID = models.AutoField(verbose_name='locationID',primary_key=True, default=0)
    locationName = models.CharField(verbose_name='locationName', max_length=45)
    parentLocID = models.ForeignKey('self', verbose_name='parentLocationID', on_delete=models.CASCADE, blank=True, null=True)


class HouseHold(models.Model):
    householdID = models.CharField(verbose_name='householdID', max_length=35, primary_key=True)
    parentLocID = models.ForeignKey(Location, verbose_name='clusterID', on_delete=models.CASCADE)
    enumeratorID = models.ForeignKey(Enumerator, verbose_name='enumeratorID', max_length=100, on_delete=models.CASCADE)
    date = models.CharField(max_length=35, blank=False)
    village_street_name = models.CharField(verbose_name='village_street_name', max_length=100, blank=True)
    gps_latitude = models.CharField(verbose_name='gps', max_length=70)
    gps_longitude = models.CharField(verbose_name='gps', max_length=70)
    availability = models.CharField(verbose_name='availability', max_length=70)
    reason_refusal = models.CharField(verbose_name='reasonforrefusal', blank=True, null=True, max_length=500)
    visit_num = models.IntegerField(verbose_name='visit_num', blank=True)
    key_informer = models.CharField(verbose_name='key_informer', max_length=45)
    tel1_num = models.CharField(verbose_name='tel1_num', max_length=30, blank=True)
    tel1_owner = models.CharField(verbose_name='tel1_owner', max_length=45, blank=True)
    tel2_num = models.CharField(verbose_name='tel2_num', max_length=30, blank=True)
    tel2_owner = models.CharField(verbose_name='tel2_owner', max_length=45, blank=True)
    consent = models.CharField(verbose_name='consent', max_length=30)
    a2q1 = models.CharField(verbose_name='a2q1', max_length=30)
    a2q2 = models.CharField(verbose_name='a2q2', max_length=30)
    a2q3 = models.CharField(verbose_name='a2q3', max_length=30)
    a2q4 = models.CharField(verbose_name='a2q4', max_length=30)
    a2q5 = models.CharField(verbose_name='a2q5', max_length=30)
    a2q6 = models.CharField(verbose_name='a2q6', max_length=30)
    a2q7 = models.CharField(verbose_name='a2q7', max_length=30)
    a2q8 = models.CharField(verbose_name='a2q8', max_length=30)
    a2q9 = models.CharField(verbose_name='a2q9', max_length=30)
    a2q10 = models.CharField(verbose_name='a2q10', max_length=30)
    a2q11 = models.CharField(verbose_name='a2q11', max_length=30)
    a2q12 = models.CharField(verbose_name='a2q12', max_length=30)
    a2q13 = models.CharField(verbose_name='a2q13', max_length=30)
