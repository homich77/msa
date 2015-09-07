from django.db import models


class City(models.Model):
    name = models.CharField(max_length=512)


class MainData(models.Model):
    link = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    city = models.ForeignKey(City, null=True, default=None)
    body = models.TextField()
