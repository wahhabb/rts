from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

# Create your models here.

class Publisher(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    issue_ct = models.IntegerField()
    def __str__(self):
        return self.name


class Series(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    year_began = models.IntegerField()
    notes = models.CharField(max_length=255, blank=True)
    issue_count = models.IntegerField()
    color = models.CharField(max_length=255, blank=True)
    gcd_publisher_id = models.ForeignKey(Publisher)
    slug = models.SlugField()
    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(max_length=255)
    slug = models.SlugField()
    def __str__(self):
        return self.genre


class Tag(models.Model):
    name = models.CharField(max_length=31)
    slug = models.SlugField()
    def __str__(self):
        return self.name


class Issue(models.Model):
    gcd_id = models.IntegerField()
    catalog_id = models.CharField(max_length=255, blank=True)
    gcd_series_id = models.ForeignKey(Series, verbose_name="Title")
    volume = models.CharField(max_length=255, blank=True)
    number = models.IntegerField(verbose_name='Issue No.')
    issue_text = models.CharField(max_length=255, blank=True)
    publication_date = models.CharField(max_length=255, blank=True)
    gcd_notes = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    grade = models.CharField(max_length=255)
    grade_notes = models.CharField(max_length=255, blank=True)
    cover_image = models.CharField(max_length=255)
    image_scanned = models.BooleanField()
    indicia_date = models.CharField(max_length=255, blank=True)
    inserts = models.CharField(max_length=255, blank=True)
    si = models.CharField(max_length=255, blank=True)
    added_date = models.DateTimeField(default=datetime.now)
    genre_id = models.ForeignKey(Genre, blank=True, null=True, verbose_name='Genre')
    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=63)
    sold_date = models.DateTimeField(null=True, blank=True)
    def get_absolute_url(self):
        return reverse('issue_detail', kwargs={'cat_id': self.pk})
    def __str__(self):
        return self.catalog_id + ' ' + self.gcd_series_id.name + ' #' + str(self.number)