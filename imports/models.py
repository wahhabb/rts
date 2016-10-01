# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class GcdBrand(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('GcdPublisher', models.DO_NOTHING, blank=True, null=True)
    year_began = models.IntegerField(blank=True, null=True)
    year_ended = models.IntegerField(blank=True, null=True)
    notes = models.TextField()
    url = models.CharField(max_length=255)
    issue_count = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reserved = models.IntegerField()
    deleted = models.IntegerField()
    year_began_uncertain = models.IntegerField()
    year_ended_uncertain = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gcd_brand'

#
# class GcdBrandEmblemGroup(models.Model):
#     brand = models.ForeignKey(GcdBrand, models.DO_NOTHING)
#     brandgroup = models.ForeignKey('GcdBrandGroup', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_brand_emblem_group'
#         unique_together = (('brand', 'brandgroup'),)
#
#
# class GcdBrandGroup(models.Model):
#     name = models.CharField(max_length=255)
#     year_began = models.IntegerField(blank=True, null=True)
#     year_ended = models.IntegerField(blank=True, null=True)
#     year_began_uncertain = models.IntegerField()
#     year_ended_uncertain = models.IntegerField()
#     notes = models.TextField()
#     url = models.CharField(max_length=255)
#     reserved = models.IntegerField()
#     created = models.DateTimeField()
#     modified = models.DateTimeField()
#     deleted = models.IntegerField()
#     parent = models.ForeignKey('GcdPublisher', models.DO_NOTHING)
#     issue_count = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_brand_group'
#
#
# class GcdBrandUse(models.Model):
#     publisher = models.ForeignKey('GcdPublisher', models.DO_NOTHING)
#     emblem = models.ForeignKey(GcdBrand, models.DO_NOTHING)
#     year_began = models.IntegerField(blank=True, null=True)
#     year_ended = models.IntegerField(blank=True, null=True)
#     year_began_uncertain = models.IntegerField()
#     year_ended_uncertain = models.IntegerField()
#     notes = models.TextField()
#     reserved = models.IntegerField()
#     created = models.DateField()
#     modified = models.DateField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_brand_use'
#
#
class GcdIndiciaPublisher(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('GcdPublisher', models.DO_NOTHING)
    country = models.ForeignKey('StddataCountry', models.DO_NOTHING)
    year_began = models.IntegerField(blank=True, null=True)
    year_ended = models.IntegerField(blank=True, null=True)
    is_surrogate = models.IntegerField()
    notes = models.TextField()
    url = models.CharField(max_length=255)
    issue_count = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reserved = models.IntegerField()
    deleted = models.IntegerField()
    year_began_uncertain = models.IntegerField()
    year_ended_uncertain = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gcd_indicia_publisher'


class GcdIssue(models.Model):
    number = models.CharField(max_length=50)
    volume = models.CharField(max_length=50)
    no_volume = models.IntegerField()
    display_volume_with_number = models.IntegerField()
    series = models.ForeignKey('GcdSeries', models.DO_NOTHING)
    indicia_publisher = models.ForeignKey(GcdIndiciaPublisher, models.DO_NOTHING, blank=True, null=True)
    indicia_pub_not_printed = models.IntegerField()
    brand = models.ForeignKey(GcdBrand, models.DO_NOTHING, blank=True, null=True)
    no_brand = models.IntegerField()
    publication_date = models.CharField(max_length=255)
    key_date = models.CharField(max_length=10)
    sort_code = models.IntegerField()
    price = models.CharField(max_length=255)
    page_count = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    page_count_uncertain = models.IntegerField()
    indicia_frequency = models.CharField(max_length=255)
    no_indicia_frequency = models.IntegerField()
    editing = models.TextField()
    no_editing = models.IntegerField()
    notes = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reserved = models.IntegerField()
    deleted = models.IntegerField()
    is_indexed = models.IntegerField()
    isbn = models.CharField(max_length=32)
    valid_isbn = models.CharField(max_length=13)
    no_isbn = models.IntegerField()
    variant_of = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    variant_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=38)
    no_barcode = models.IntegerField()
    title = models.CharField(max_length=255)
    no_title = models.IntegerField()
    on_sale_date = models.CharField(max_length=10)
    on_sale_date_uncertain = models.IntegerField()
    rating = models.CharField(max_length=255)
    no_rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gcd_issue'
        unique_together = (('series', 'sort_code'),)


# class GcdIssueReprint(models.Model):
#     origin_issue = models.ForeignKey(GcdIssue, models.DO_NOTHING)
#     target_issue = models.ForeignKey(GcdIssue, models.DO_NOTHING)
#     notes = models.TextField()
#     reserved = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_issue_reprint'
#

class GcdPublisher(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('StddataCountry', models.DO_NOTHING)
    year_began = models.IntegerField(blank=True, null=True)
    year_ended = models.IntegerField(blank=True, null=True)
    notes = models.TextField()
    url = models.CharField(max_length=255)
    is_master = models.IntegerField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    imprint_count = models.IntegerField()
    brand_count = models.IntegerField()
    indicia_publisher_count = models.IntegerField()
    series_count = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    issue_count = models.IntegerField()
    reserved = models.IntegerField()
    deleted = models.IntegerField()
    year_began_uncertain = models.IntegerField()
    year_ended_uncertain = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gcd_publisher'

    def __str__(self):
        return self.name


# class GcdReprint(models.Model):
#     origin = models.ForeignKey('GcdStory', models.DO_NOTHING)
#     target = models.ForeignKey('GcdStory', models.DO_NOTHING)
#     notes = models.TextField()
#     reserved = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_reprint'
#
#
# class GcdReprintFromIssue(models.Model):
#     origin_issue = models.ForeignKey(GcdIssue, models.DO_NOTHING)
#     target = models.ForeignKey('GcdStory', models.DO_NOTHING)
#     notes = models.TextField()
#     reserved = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_reprint_from_issue'
#
#
# class GcdReprintToIssue(models.Model):
#     origin = models.ForeignKey('GcdStory', models.DO_NOTHING)
#     target_issue = models.ForeignKey(GcdIssue, models.DO_NOTHING)
#     notes = models.TextField()
#     reserved = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_reprint_to_issue'
#

class GcdSeries(models.Model):
    name = models.CharField(max_length=255)
    sort_name = models.CharField(max_length=255)
    format = models.CharField(max_length=255)
    year_began = models.IntegerField()
    year_began_uncertain = models.IntegerField()
    year_ended = models.IntegerField(blank=True, null=True)
    year_ended_uncertain = models.IntegerField()
    publication_dates = models.CharField(max_length=255)
    first_issue = models.ForeignKey(GcdIssue, models.DO_NOTHING, blank=True, null=True, related_name='first_issue')
    last_issue = models.ForeignKey(GcdIssue, models.DO_NOTHING, blank=True, null=True, related_name='last_issue')
    is_current = models.IntegerField()
    publisher = models.ForeignKey(GcdPublisher, models.DO_NOTHING)
    country = models.ForeignKey('StddataCountry', models.DO_NOTHING)
    language = models.ForeignKey('StddataLanguage', models.DO_NOTHING)
    tracking_notes = models.TextField()
    notes = models.TextField()
    publication_notes = models.TextField()
    has_gallery = models.IntegerField()
    open_reserve = models.IntegerField(blank=True, null=True)
    issue_count = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    reserved = models.IntegerField()
    deleted = models.IntegerField()
    has_indicia_frequency = models.IntegerField()
    has_isbn = models.IntegerField()
    has_barcode = models.IntegerField()
    has_issue_title = models.IntegerField()
    has_volume = models.IntegerField()
    is_comics_publication = models.IntegerField()
    color = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    paper_stock = models.CharField(max_length=255)
    binding = models.CharField(max_length=255)
    publishing_format = models.CharField(max_length=255)
    has_rating = models.IntegerField()
    publication_type_id = models.IntegerField(blank=True, null=True)
    is_singleton = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'gcd_series'

    def __str__(self):
        return self.name

# class GcdStory(models.Model):
#     title = models.CharField(max_length=255)
#     title_inferred = models.IntegerField()
#     feature = models.CharField(max_length=255)
#     sequence_number = models.IntegerField()
#     page_count = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
#     issue = models.ForeignKey(GcdIssue, models.DO_NOTHING)
#     script = models.TextField()
#     pencils = models.TextField()
#     inks = models.TextField()
#     colors = models.TextField()
#     letters = models.TextField()
#     editing = models.TextField()
#     genre = models.CharField(max_length=255)
#     characters = models.TextField()
#     synopsis = models.TextField()
#     reprint_notes = models.TextField()
#     created = models.DateTimeField()
#     modified = models.DateTimeField()
#     notes = models.TextField()
#     no_script = models.IntegerField()
#     no_pencils = models.IntegerField()
#     no_inks = models.IntegerField()
#     no_colors = models.IntegerField()
#     no_letters = models.IntegerField()
#     no_editing = models.IntegerField()
#     page_count_uncertain = models.IntegerField()
#     type = models.ForeignKey('GcdStoryType', models.DO_NOTHING)
#     job_number = models.CharField(max_length=25)
#     reserved = models.IntegerField()
#     deleted = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_story'
#
#
# class GcdStoryType(models.Model):
#     name = models.CharField(unique=True, max_length=50)
#     sort_code = models.IntegerField(unique=True)
#
#     class Meta:
#         managed = False
#         db_table = 'gcd_story_type'


class StddataCountry(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'stddata_country'


class StddataLanguage(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'stddata_language'


class TblComics(models.Model):
    is_done = models.CharField(max_length=1)
    cat_id = models.IntegerField()
    name = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    series = models.CharField(max_length=255)
    gcd_series_id = models.IntegerField()
    gcd_series_url = models.CharField(max_length=255)
    gcd_issue_id = models.IntegerField()
    gcd_issue_url = models.CharField(max_length=255)
    gcd_publisher_id = models.IntegerField()
    gcd_publisher_url = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    gcd_publisher_id_2 = models.IntegerField()
    gcd_publisher_url_2 = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)
    thumbnail2 = models.CharField(max_length=255)
    thumbnail3 = models.CharField(max_length=255)
    thumbnail4 = models.CharField(max_length=255)
    thumbnail5 = models.CharField(max_length=255)
    thumbnail6 = models.CharField(max_length=255)
    thumbnail7 = models.CharField(max_length=255)
    thumbnail8 = models.CharField(max_length=255)
    thumbnail9 = models.CharField(max_length=255)
    thumbnail10 = models.CharField(max_length=255)
    bigimage = models.CharField(db_column='bigImage', max_length=255)  # Field name made lowercase.
    scarcity_note = models.CharField(db_column='Scarcity_Note', max_length=255)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255)  # Field name made lowercase.
    title_notes = models.CharField(db_column='Title_Notes', max_length=255)  # Field name made lowercase.
    issue_notes = models.CharField(max_length=255)
    grade_notes = models.CharField(db_column='Grade_Notes', max_length=255)  # Field name made lowercase.
    indicia_date = models.CharField(db_column='Indicia_Date', max_length=255)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255)  # Field name made lowercase.
    catalog_no = models.CharField(db_column='Catalog_No', max_length=255)  # Field name made lowercase.
    mark = models.CharField(db_column='Mark', max_length=255)  # Field name made lowercase.
    issue_text = models.CharField(db_column='Issue_Text', max_length=255)  # Field name made lowercase.
    edition = models.CharField(db_column='Edition', max_length=255)  # Field name made lowercase.
    sort_title = models.CharField(db_column='Sort_Title', max_length=255)  # Field name made lowercase.
    near_grade = models.CharField(db_column='Near_Grade', max_length=255)  # Field name made lowercase.
    inserts = models.CharField(db_column='Inserts', max_length=255)  # Field name made lowercase.
    issue = models.IntegerField()
    ceritifcate_no = models.CharField(db_column='Ceritifcate_No', max_length=255)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    nm_price = models.CharField(db_column='NM_Price', max_length=255)  # Field name made lowercase.
    cover_price = models.CharField(db_column='Cover_price', max_length=255)  # Field name made lowercase.
    si = models.CharField(db_column='SI', max_length=255)  # Field name made lowercase.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nm = models.CharField(db_column='NM', max_length=255)  # Field name made lowercase.
    single_quantity = models.CharField(db_column='Single_Quantity', max_length=255)  # Field name made lowercase.
    cost = models.CharField(db_column='Cost', max_length=255)  # Field name made lowercase.
    overstreet_0 = models.CharField(db_column='Overstreet_0', max_length=255)  # Field name made lowercase.
    packs = models.CharField(db_column='Packs', max_length=255)  # Field name made lowercase.
    no_per_pack = models.CharField(db_column='No_Per_Pack', max_length=255)  # Field name made lowercase.
    overstreet_01_price = models.CharField(db_column='Overstreet_01_Price', max_length=255)  # Field name made lowercase.
    bar_code_price = models.CharField(db_column='Bar_Code_Price', max_length=255)  # Field name made lowercase.
    title_code = models.CharField(db_column='Title_Code', max_length=255)  # Field name made lowercase.
    overstreet_02 = models.CharField(db_column='Overstreet_02', max_length=255)  # Field name made lowercase.
    vol_no = models.IntegerField(db_column='Vol_No')  # Field name made lowercase.
    collection_no = models.CharField(db_column='Collection_No', max_length=255)  # Field name made lowercase.
    numerical_grade = models.DecimalField(db_column='Numerical_Grade', max_digits=10, decimal_places=3)  # Field name made lowercase.
    overstreet_03 = models.CharField(db_column='Overstreet_03', max_length=255)  # Field name made lowercase.
    overstreet_04 = models.CharField(db_column='Overstreet_04', max_length=255)  # Field name made lowercase.
    variance = models.CharField(max_length=255)
    publication = models.CharField(max_length=255)
    story = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    inker = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    type_of_cover = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    first_appearance = models.CharField(max_length=255)
    origin_of_story = models.CharField(max_length=255)
    page_quality = models.CharField(max_length=255)
    is_featured = models.CharField(max_length=1)
    description = models.CharField(max_length=255)
    pagetitle = models.CharField(db_column='pageTitle', max_length=255)  # Field name made lowercase.
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=255)
    sortorder = models.IntegerField(db_column='sortOrder')  # Field name made lowercase.
    auto_url = models.CharField(max_length=1)
    is_active = models.CharField(max_length=1)
    added_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_comics'

