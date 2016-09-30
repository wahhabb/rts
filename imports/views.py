from django.shortcuts import render
from django.views.generic.list import  View
from django.core.exceptions import ObjectDoesNotExist
import logging
import os.path
from openpyxl import load_workbook
from imports.models import *
from comix.models import Publisher, Series, Issue


logger = logging.getLogger(__name__)

# Create your views here.
class PublisherFixView(View):
    template_name = 'imports/fixtest.html'
    gcd_series_recs = None

    def get(self, request):
        wb = load_workbook(filename="data/PubFix.xlsx")
        wb.guess_types = True
        sheet = wb.active
        cells = sheet['A4':'B62']
        fixes = {}
        items = [('Catalog No', 'Name', 'Problem')]
        for row in cells:
            fixes[row[0].value] = row[1].value

        issues = TblComics.objects.all()
        # limit for testing
        issues = issues.filter(status="test")

        for tbl_issue in issues:
            # Determine if already in database
            try:
                c_issue = Issue.objects.get(catalog_id = tbl_issue.catalog_no)
                if tbl_issue.is_active == 'N':
                    c_issue.status = 'N'
                else:
                    c_issue.status = 'available'
                c_issue.save()
                tbl_issue.is_done = 'Y'
                tbl_issue.status = 'available'
                tbl_issue.save()
                continue  # not necessary, just for clarity

            except ObjectDoesNotExist:
                # add new entry
                issue = Issue()

                # Fill in entries from input. Some may need to be fixed
                # Note: there can be multiple records for the same issue in different grades.
                issue.catalog_id = tbl_issue.catalog_no
                issue.volume = tbl_issue.vol_no
                issue.number = tbl_issue.issue
                issue.issue_text = tbl_issue.issue_text
                issue.notes = tbl_issue.issue_notes
                issue.grade = tbl_issue.grade
                issue.grade_notes = tbl_issue.grade_notes
                issue.cover_image = tbl_issue.thumbnail
                issue.image_scanned = 0
                issue.indicia_date = tbl_issue.indicia_date
                issue.inserts = tbl_issue.inserts
                issue.si = tbl_issue.si
                issue.added_date = tbl_issue.added_date
                issue.price = tbl_issue.price
                issue.quantity = int('0' + tbl_issue.packs) * int('0' + tbl_issue.no_per_pack) + \
                    int(tbl_issue.single_quantity)
                issue.status = tbl_issue.status
                issue.gcd_id = tbl_issue.gcd_issue_id
                if tbl_issue.is_active == 'N':
                    issue.status = 'N'

                if tbl_issue.gcd_series_id == 0:
                    # Find series from title
                    self.gcd_series_recs = GcdSeries.objects.filter(name=tbl_issue.name)
                    series_ct = len(self.gcd_series_recs)
                    if series_ct == 0:
                        # failed to get match on name, drop item
                        items.append((issue.catalog_id, tbl_issue.name, "No match on name"))
                        continue
                    elif series_ct > 1:
                        # Need to find publisher
                        if tbl_issue.gcd_publisher_id > 0:
                            gcd_series = self.gcd_series_recs.get(publisher_id=tbl_issue.gcd_publisher_id,
                                                                  first_issue_id__lte=tbl_issue.issue,
                                                                  last_issue_id__gte=tbl_issue.issue)
                        else:
                            # look up publisher based on name
                            try:
                                gcd_publisher = GcdPublisher.objects.get(name=tbl_issue.publisher)
                            except ObjectDoesNotExist:
                                publisher_id = fixes.get(tbl_issue.publisher)
                                if publisher_id == None:
                                    items.append((issue.catalog_id, tbl_issue.name, "Publisher not found"))
                                    continue
                                else:
                                    gcd_publisher = GcdPublisher.objects.get(pk = publisher_id)
                                try:
                                    publisher = Publisher.objects.get(pk = gcd_publisher.id)
                                except ObjectDoesNotExist:
                                    # Need to add publisher
                                    publisher = Publisher(id=gcd_publisher.id, gcd_id=gcd_publisher.id,
                                                          name=gcd_publisher.name, issue_ct=gcd_publisher.issue_count)
                                    publisher.save()


                                # Now get series based on publisher
                                gcd_series = self.gcd_series_recs.get(publisher_id=tbl_issue.gcd_publisher_id,
                                                                      first_issue_id__lte=tbl_issue.issue,
                                                                      last_issue_id__gte=tbl_issue.issue)
                                issue.gcd_series_id = gcd_series.id
                    else:
                        # just one series matches
                        issue.gcd_series_id = self.gcd_series_recs[0].id
                else:       # We have series ID
                    # Get or create series record
                    try:
                        series = Series.objects.get(pk = tbl_issue.gcd_series_id)
                    except ObjectDoesNotExist:
                        series = Series()
                        series.id = series.gcd_id = issue.gcd_series_id
                        gcd_series = GcdSeries.objects.get(pk = series.id) # shouldn't fail
                        series.name = gcd_series.name
                        series.sort_name = gcd_series.sort_name
                        series.year_began = gcd_series.year_began
                        series.notes = gcd_series.notes
                        series.issue_count = gcd_series.issue_count
                        series.color = gcd_series.color
                        series.gcd_publisher_id = gcd_series.publisher_id
                        series.save()
                    # ToDo: Delete genre?
                    # issue.genre_id =
                issue.gcd_series_id = series

                gcd_issue = GcdIssue.objects.get(pk=tbl_issue.gcd_issue_id)
                issue.publication_date = gcd_issue.publication_date
                issue.gcd_notes = gcd_issue.notes
                # Verify Publisher in database or create new
                try:
                    self.gcd_series_recs = GcdSeries.objects.filter(name=tbl_issue.name)
                    publisher = Publisher.objects.get(pk=self.gcd_series_recs[0].publisher_id)
                except ObjectDoesNotExist:
                    # Need to add publisher. ToDo: Duplicate code from above
                    publisher = Publisher(id=gcd_publisher.id, gcd_id=gcd_publisher.id,
                                          name=gcd_publisher.name, issue_ct=gcd_publisher.issue_count)
                    publisher.save()

                issue.save()

                # Now go after cover image
                if issue.cover_image == "":
                    issue.cover_image = '/static/thumbnails/' + str(issue.gcd_id) + '.jpg'
                if not os.path.isfile(issue.cover_image):
                    self.scrape_image(issue.gcd_id)
                tbl_issue.is_done = 'Y' # Mark record as completed
                tbl_issue.status = 'available'
                tbl_issue.save()

        context = {'errors': items,
                   }
        return render(
            request, self.template_name, context
        )

    def scrape_image(self, gcd_issue_id):
        import urllib.request
        from bs4 import BeautifulSoup
        import re
        from PIL import Image

        # Get cover from "http://www.comics.org/issue/" + gcd_issue_id + '/cover/4/'
        with urllib.request.urlopen('http://www.comics.org/issue/' + str(gcd_issue_id) + '/cover/4/') as response:
           html = response.read()
        soup = BeautifulSoup(html)
        img = soup.find('img', 'cover_img')
        matches = re.match(r'.+src="(http.+/(\d+.jpg)).+', str(img))
        filename = matches.group(1)
        saved_filename = 'comix/static/bigImages/' + matches.group(2)
        urllib.request.urlretrieve(filename, saved_filename)
        # Now create thumbnail
        size = (100, 156)
        thumb_filename = 'comix/static/thumbnails/' + matches.group(2)
        im = Image.open(saved_filename)
        im.thumbnail(size)
        im.save(thumb_filename, "JPEG")

