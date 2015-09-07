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


class Proxy(models.Model):
    """
    status:
    0 - not check
    -1 - failed
    > 0 - secs
    """
    address = models.CharField(max_length=30, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    check_date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
