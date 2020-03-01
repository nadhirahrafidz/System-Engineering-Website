from django.db import models


class APIClient(models.Model):
    access_token = models.CharField(max_length=255, blank=True)
    expires_on = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
