from django.db import models
from datetime import date

class Enumerator(models.Model):
    enumeratorID = models.CharField(verbose_name='enumeratorID', primary_key=True, unique=True, max_length=100)
    CHOICES = (
        ('MR', 'Mr'),
        ('MRS', 'Mrs'),
        ('MISS', 'Miss'),
        ('MS', 'MS'),
        ('DR', 'Dr'),
    )
    prefix = models.CharField(verbose_name='prefix', max_length=10, choices=CHOICES)
    firstName = models.CharField(verbose_name='firstName', max_length=45)
    lastName = models.CharField(verbose_name='lastName', max_length=45)
    suffix = models.CharField(verbose_name='suffix', max_length=45, blank=True)
    organization = models.CharField(verbose_name='organization', max_length=100, blank=True)
    date_of_birth = models.CharField(max_length=35)
    active_flag = models.BooleanField(verbose_name='active_flag', default=True)
    username = models.CharField(verbose_name='username', max_length=100)
    email = models.EmailField(verbose_name='email', max_length=100)

