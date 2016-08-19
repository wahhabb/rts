from django.db import models

# Create your models here.

class Publisher(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    def __str__(self):
        return self.name


class Series(models.Model):
    gcd_id = models.IntegerField()
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    year_began = models.IntegerField()
    notes = models.CharField(max_length=255)
    issue_count = models.IntegerField()
    color = models.CharField(max_length=255)
    gcd_publisher_id = models.ForeignKey(Publisher)
    slug = models.SlugField()


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
    catalog_id = models.CharField(max_length=255)
    gcd_series_id = models.ForeignKey(Series)
    volume = models.CharField(max_length=255)
    number = models.IntegerField()
    issue_text = models.CharField(max_length=255)
    publication_date = models.CharField(max_length=255)
    gcd_notes = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    grade_notes = models.CharField(max_length=255)
    cover_image = models.CharField(max_length=255)
    image_scanned = models.BooleanField()
    indicia_date = models.CharField(max_length=255)
    inserts = models.CharField(max_length=255)
    si = models.CharField(max_length=255)
    added_date = models.DateTimeField()
    genre_id = models.ForeignKey(Genre)
    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=63)
    sold_date = models.DateTimeField(null=True)
