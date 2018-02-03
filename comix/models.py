from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import re


# Create your models here.

class PubCount(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField()
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name)[:49]
        super(PubCount, self).save(*args, **kwargs)

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

class Image(models.Model):
    is_scanned = models.BooleanField()
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name


class Issue(models.Model):
    title = models.CharField(max_length=255, default='Not yet titled')
    sort_title = models.CharField(max_length=255, default='not-yet-titled')
    in_gcd_flag = models.BooleanField(default=True)
    catalog_id = models.CharField(max_length=255, blank=True, unique=True)
    year_begun = models.IntegerField(default=0)
    publisher_name = models.CharField(max_length=255, blank=True)
    volume = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(verbose_name='Issue No.')
    issue_text = models.CharField(max_length=255, blank=True)
    edition = models.CharField(max_length=255, blank=True, default='')
    notes = models.TextField(blank=True)
    scarcity_notes = models.TextField(blank=True)   # Previously called si
    grade = models.CharField(max_length=255)
    grade_notes = models.CharField(max_length=255, blank=True)
    image_scanned = models.BooleanField()
    indicia_date = models.CharField(max_length=255, blank=True)
    inserts = models.CharField(max_length=255, blank=True)
    added_date = models.DateTimeField(default=timezone.now)
    genre = models.ForeignKey(Genre, blank=True, null=True, verbose_name='Genre', on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    sold_date = models.DateTimeField(null=True, blank=True)
    show_number = models.CharField(max_length=20, blank=True)
    numerical_grade = models.DecimalField(max_digits=3, decimal_places=2)
    hrn_number = models.IntegerField(blank=True, null=True)  # For Classics Illustrated
    gcd_id = models.IntegerField()
    gcd_series_id = models.IntegerField()

    @property
    def notes_preview(self):
        max_len = 43
        issue_text = self.issue_text
        if len(issue_text) > 0:
            issue_text += '.'
        inserts = self.inserts
        if len(inserts) > 0:
            inserts += '.'
        all_notes = ' '.join([issue_text, self.edition, inserts, self.notes,
                              self.scarcity_notes, self.grade_notes ])
        all_notes = re.sub('\s+', ' ', all_notes)[:max_len]
        if len(all_notes) >= max_len:
            all_notes += '...'
        if all_notes == ' ':
            all_notes = ''
        return all_notes

    @property
    def all_notes(self):
        issue_text = self.issue_text
        if len(issue_text) > 0:
            issue_text += '.'
        inserts = self.inserts
        if len(inserts) > 0:
            inserts += '.'
        all_notes = ' '.join([issue_text, self.edition, inserts, self.notes,
                        self.scarcity_notes, self.grade_notes ])
        all_notes = re.sub('\s+', ' ', all_notes)
        if all_notes == ' ':
            all_notes = ''
        return all_notes

    @property
    def long_title(self):
        return self.title + ' — ' + str(self.year_begun) + ' Series'


    def get_absolute_url(self):
        return reverse('issue_detail', kwargs={'cat_id': self.catalog_id})

    def __str__(self):
        if self.volume == '':
            return self.catalog_id + ' ' + self.title + ' #' + str(self.show_number)
        else:
            return self.catalog_id + ' ' + self.title + ' Vol. ' + self.volume + ' #' + str(self.show_number)

