from django.db import models

# Create your models here.

class Publisher(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=251)
    slug = models.CharField(max_length=63)


class Series(models.Model):
    pass

class Issues(models.Model):
    pass
