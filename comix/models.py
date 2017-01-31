from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify
import re


# Create your models here.

class Publisher(models.Model):
    gcd_id = models.IntegerField()
    in_gcd_flag = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    issue_ct = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:49]
        super(Publisher, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Series(models.Model):
    gcd_id = models.IntegerField()
    in_gcd_flag = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    year_began = models.IntegerField()
    notes = models.TextField(blank=True)
    issue_count = models.IntegerField()
    color = models.CharField(max_length=255, blank=True)
    gcd_publisher = models.ForeignKey(Publisher)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:49]
        super(Series, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.genre)[:49]
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.genre


class Tag(models.Model):
    name = models.CharField(max_length=31)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:49]
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Issue(models.Model):
    gcd_id = models.IntegerField()
    in_gcd_flag = models.BooleanField(default=True)
    catalog_id = models.CharField(max_length=255, blank=True, unique=True)
    gcd_series = models.ForeignKey(Series, verbose_name="Title")
    publisher_name = models.CharField(max_length=255, blank=True)
    volume = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(verbose_name='Issue No.')
    issue_text = models.CharField(max_length=255, blank=True)
    edition = models.CharField(max_length=255, blank=True, default='')
    publication_date = models.CharField(max_length=255, blank=True)
    gcd_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    scarcity_notes = models.TextField(blank=True)   # Previously called si
    grade = models.CharField(max_length=255)
    grade_notes = models.CharField(max_length=255, blank=True)
    cover_image = models.CharField(max_length=255)
    image_scanned = models.BooleanField()
    indicia_date = models.CharField(max_length=255, blank=True)
    inserts = models.CharField(max_length=255, blank=True)
    added_date = models.DateTimeField(default=timezone.now)
    genre = models.ForeignKey(Genre, blank=True, null=True, verbose_name='Genre')
    tags = models.ManyToManyField(Tag, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=63)
    sold_date = models.DateTimeField(null=True, blank=True)
    variants = models.CharField(max_length=255, null=True, blank=True)
    show_number = models.CharField(max_length=20, blank=True)
    numerical_grade = models.DecimalField(max_digits=3, decimal_places=2)
    hrn_number = models.IntegerField(blank=True, null=True)  # For Classics Illustrated

    @property
    def notes_preview(self):
        all_notes = ' '.join([self.issue_text, self.edition, self.inserts, self.notes,
                        self.scarcity_notes, self.grade_notes ])[:120]
        if len(all_notes) > 119:
            all_notes += '...'
        all_notes = re.sub('\s+', ' ', all_notes)
        if all_notes == ' ':
            all_notes = ''
        return all_notes

    @property
    def gcd_notes_preview(self):
        notes = self.gcd_notes[:100]
        if len(notes) > 99:
            notes += '...'
        return notes

    @property
    def all_notes(self):
        all_notes = ' '.join([self.issue_text, self.edition, self.inserts, self.notes,
                        self.scarcity_notes, self.grade_notes ])
        all_notes = re.sub('\s+', ' ', all_notes)
        if all_notes == ' ':
            all_notes = ''
        return all_notes


    def get_absolute_url(self):
        return reverse('issue_detail', kwargs={'cat_id': self.catalog_id})

    def __str__(self):
        if self.volume == '':
            return self.catalog_id + ' ' + self.gcd_series.name + ' #' + str(self.show_number)
        else:
            return self.catalog_id + ' ' + self.gcd_series.name + ' Vol. ' + self.volume + ' #' + str(self.show_number)

