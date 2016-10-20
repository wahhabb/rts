from django.shortcuts import render
from django.views.generic.list import  View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging
import os.path
from imports.models import *
from comix.models import Publisher, Series, Issue


def scrape_images(gcd_issue_id):
    import urllib.request
    from bs4 import BeautifulSoup
    import re
    from PIL import Image
    from time import sleep

    sleep(1)  # Avoid Error 509 Bandwidth limitation
    filenames = []

    # Get cover from "http://www.comics.org/issue/" + gcd_issue_id + '/cover/4/'
    with urllib.request.urlopen('http://www.comics.org/issue/' + str(gcd_issue_id) + '/cover/4/') as response:
        html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.find_all('img', 'cover_img')
    for img in imgs:
        matches = re.match(r'.+src="(http.+/(\d+.jpg)).+', str(img))
        if matches is None:
            return ""  # Missing cover on comics.org
        src_filename = matches.group(1)
        filename = matches.group(2)
        filenames.append(filename)
        saved_filename = 'comix/static/bigImages/' + filename
        if not os.path.isfile(saved_filename):
            print("Scraping image issue", gcd_issue_id)
            urllib.request.urlretrieve(src_filename, saved_filename)
            sleep(1)
            # Now create thumbnail
            size = (100, 156)
            thumb_filename = 'comix/static/thumbnails/' + filename
            im = Image.open(saved_filename)
            im.thumbnail(size)
            im.save(thumb_filename, "JPEG")
    return filenames


def debug(str1, str2=''):
    print(str(str1), str(str2))


class FindVariantView(View):
    template_name = 'imports/variants.html'
    gcd_series_recs = None

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        useimg = request.POST.get('useimg', '')
        if useimg == '':    # We;re getting first submit to show images
            images = []
            error = ''
            cat_id = request.POST['catalog-no']
            try:
                issue = Issue.objects.get(catalog_id=cat_id)
                if not issue.variants > "":
                    error = "No variants on issue"
                else:
                    images = scrape_images(issue.gcd_id)
                    debug(images)

            except ObjectDoesNotExist:
                error = "Not Found"
                issue = None

            context = {
                'title': str(issue),
                'error': error,
                'images': images,
                'cat_id': cat_id,
            }
        else:
            # User clicked so select an image,so update it on record and clear variant field
            issue = Issue.objects.get(catalog_id=request.POST.get('usecat'))
            issue.cover_image = useimg.split('/')[3] # strip off name.jpg
            # issue.variants = ''
            issue.save()
            context = {
                'title': str(issue) + ' was saved!',
                'error': '',
                'images': [],
                'cat_id': '',
            }


        return render(
            request, self.template_name, context
        )

            #         # add new entry
        #         debug('creating issue:', Comic.catalog_no)
        #         issue = Issue()
        #
        #         # Fill in entries from input. Some may need to be fixed
        #         # Note: there can be multiple records for the same issue in different grades.
        #         issue.catalog_id = Comic.catalog_no
        #         issue.volume = Comic.vol_no
        #         issue.number = Comic.issue
        #         issue.issue_text = Comic.issue_text
        #         issue.notes = Comic.issue_notes
        #         issue.grade = Comic.grade
        #         issue.grade_notes = Comic.grade_notes
        #         issue.image_scanned = 0
        #         issue.inserts = Comic.inserts
        #         issue.si = Comic.si
        #         issue.added_date = timezone.now()
        #         issue.price = Comic.price
        #         issue.quantity = Comic.quantity
        #         issue.status = 'available'
        #
        #         # Find series from title and year begun
        #         self.gcd_series_recs = GcdSeries.objects.filter(Q(name=Comic.name) | Q(sort_name=Comic.name))
        #         self.gcd_series_recs = self.gcd_series_recs.filter(country_id=225, year_began=Comic.year)
        #         series_ct = len(self.gcd_series_recs)
        #         debug('series_ct', str(series_ct))
        #         if series_ct == 0:
        #             # failed to get match on name, drop item
        #             messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "No match on name"))
        #             continue
        #         elif series_ct > 1:
        #             # Let's look for a unique match on title and issue #
        #             gcd_issue_recs = GcdIssue.objects.filter(Q(series_id__name=Comic.name) |
        #                                                      Q(series_id__sort_name=Comic.name))
        #             gcd_issue_recs = gcd_issue_recs.filter(number=Comic.issue)
        #             issue_ct = len(gcd_issue_recs)
        #             if issue_ct == 0:
        #                 messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
        #                                  "No match on issue name and number"))
        #                 continue
        #             elif issue_ct == 1:
        #                 # assume we found our match
        #                 gcd_issue = gcd_issue_recs[0]
        #                 gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
        #                 gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
        #             else: # More than one. Try to match based on publisher
        #                 tmp_issue_recs = gcd_issue_recs.filter(series_id__publisher__name=Comic.publisher)
        #                 issue_ct = len(tmp_issue_recs)
        #                 if issue_ct == 0:
        #                     messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Publisher not found"))
        #                     continue
        #                 elif issue_ct > 1: # have variants
        #                     debug('variants count:', str(issue_ct))
        #                     gcd_issue = tmp_issue_recs[0]
        #                     gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
        #                     gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
        #                     issue.variants = ''
        #                     for var_issue in tmp_issue_recs:
        #                         issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
        #                         debug('issue.variants:', issue.variants)
        #                     messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
        #                                      "Duplicate records for title, issue, publisher"))
        #                     # We are creating error message but fall through to save issue record.
        #                     # We won't display this issue because variants are present.
        #                 else:   # found our match
        #                     gcd_issue = tmp_issue_recs[0]
        #                     gcd_series = GcdSeries.objects.get(id=tmp_issue_recs[0].series_id)
        #                     gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
        #         else: # just one series_ct
        #             gcd_series = self.gcd_series_recs[0]
        #             gcd_publisher = GcdPublisher.objects.get(pk=gcd_series.publisher_id)
        #             gcd_issue_recs = GcdIssue.objects.filter(number=issue.number, series_id=gcd_series.id)
        #             if len(gcd_issue_recs) == 0:
        #                 a1 = issue.number
        #                 a2 = gcd_series.id
        #                 messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Bad issue number?"))
        #                 continue
        #             gcd_issue = gcd_issue_recs[0]
        #             # Multiple issues above are variants.
        #             if len(gcd_issue_recs) > 1:
        #                 debug('variants count:', str(len(gcd_issue_recs)))
        #                 issue.variants = ''
        #                 for var_issue in gcd_issue_recs:
        #                     issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
        #                     debug('issue.variants:', issue.variants)
        #                 messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
        #                                  "Variant issues"))
        #                 # Again, create error message but keep record
        #
        #         # Now we have gcd_series
        #
        #         # Verify Publisher in database or create new
        #         try:
        #             debug('Checking Publisher:', gcd_publisher.name)
        #             publisher = Publisher.objects.get(pk=gcd_series.publisher_id)
        #         except ObjectDoesNotExist:
        #             # Need to add publisher.
        #             publisher = Publisher(id=gcd_publisher.id, gcd_id=gcd_publisher.id,
        #                                   name=gcd_publisher.name, issue_ct=gcd_publisher.issue_count)
        #             publisher.save()
        #
        #
        #         # Get or create series record
        #         try:
        #             series = Series.objects.get(pk = gcd_series.id)
        #         except ObjectDoesNotExist:
        #             print("Creating series:", gcd_series.id, gcd_series.name)
        #             series = Series()
        #             series.id = series.gcd_id = gcd_series.id
        #             series.name = gcd_series.name
        #             series.sort_name = gcd_series.sort_name
        #             series.year_began = gcd_series.year_began
        #             series.notes = gcd_series.notes
        #             series.issue_count = gcd_series.issue_count
        #             series.color = gcd_series.color
        #             series.gcd_publisher = publisher
        #             series.save()
        #             print("Saved series:", series.pk)
        #         # ToDo: Set genre
        #         # issue.genre_id =
        #
        #         issue.gcd_series = series
        #         issue.publication_date = gcd_issue.publication_date
        #         issue.gcd_notes = gcd_issue.notes
        #         issue.gcd_id = gcd_issue.id
        #
        #         # Now go after cover image
        #         if issue.cover_image == "":
        #             issue.cover_image = scrape_image(issue.gcd_id)
        #
        #         # success! Save our issue
        #         issue.save()
        #         debug("Issue saved", str(issue))
        #         # tbl_issue.is_done = 'Y'  # Mark record as completed
        #         # tbl_issue.status = 'available'
        #         # tbl_issue.save()
        #
        # context = {'errors': messages,
        #            }
        # return render(
        #     request, self.template_name, context
        # )

