from django.db import models

# Create your models here.

class Publisher(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=63)


class Series(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    year_began = models.IntegerField()
    notes = models.CharField(max_length=255)
    issue_count = models.IntegerField()
    color = models.CharField(max_length=255)
    gcd_publisher_id = models.IntegerField()
    slug = models.CharField(max_length=255)

class Issues(models.Model):
    pass
