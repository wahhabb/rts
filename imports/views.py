from django.shortcuts import render
from django.views.generic.list import  View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
        messages = [('Catalog No', 'Name', 'Problem')]
        for row in cells:
            fixes[row[0].value] = row[1].value

        issues = TblComics.objects.all()

        issues = issues.filter(is_done='N')

        for tbl_issue in issues:
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


                # Temporary: Pick up series from tbl_comics. Can't use for spreadsheet
                # if tbl_issue.gcd_issue_id > 0:
                #     self.gcd_series_recs = GcdSeries.objects.filter(id = tbl_issue.gcd_issue_id)
                # else:

                # Find series from title
                self.gcd_series_recs = GcdSeries.objects.filter(name=tbl_issue.name)
                series_ct = len(self.gcd_series_recs)
                if series_ct == 0:
                    # failed to get match on name, drop item
                    if tbl_issue.gcd_series_id == 0:
                        messages.append((issue.catalog_id, tbl_issue.name, "No match on name"))
                    else:
                        messages.append((issue.catalog_id, tbl_issue.name, "Showed gcd_series_id but \nNo match on name"))
                    continue
                elif series_ct > 1:
                    # Let's look for a unique match on title and issue #
                    gcd_issue_recs = GcdIssue.objects.filter(series_id__name=tbl_issue.name, number=issue.number)
                    issue_ct = len(gcd_issue_recs)
                    if issue_ct == 0:
                        messages.append((issue.catalog_id, tbl_issue.name,
                                         "No match on issue name and number"))
                        continue
                    elif issue_ct == 1:
                        # assume we found our match
                        gcd_issue = gcd_issue_recs[0]
                        gcd_series = GcdSeries.objects.get(id=gcd_issue_recs[0].series_id)
                        gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                    else: # More than one. Try to match based on publisher
                        tmp_issue_recs = gcd_issue_recs.filter(series_id__publisher__name=tbl_issue.publisher)
                        issue_ct = len(tmp_issue_recs)
                        if issue_ct == 0:
                            messages.append((issue.catalog_id, tbl_issue.name, "Publisher not found"))
                            continue
                        elif issue_ct > 1:
                            messages.append((issue.catalog_id, tbl_issue.name, "Duplicate Publishers for title and issue"))
                            continue
                        else:
                            gcd_issue = tmp_issue_recs[0]
                            gcd_series = GcdSeries.objects.get(id=tmp_issue_recs[0].series_id)
                            gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                else: # just one series_ct
                    gcd_series = self.gcd_series_recs[0]
                    gcd_publisher = GcdPublisher.objects.get(pk=gcd_series.publisher_id)
                    gcd_issue_recs = GcdIssue.objects.filter(number=issue.number, series_id=gcd_series.id)
                    if len(gcd_issue_recs) == 0:
                        a1 = issue.number
                        a2 = gcd_series.id
                        messages.append((issue.catalog_id, tbl_issue.name, "Bad issue number?"))
                        continue
                    gcd_issue = gcd_issue_recs[0]
                    # ToDo: Multiple issues above are variants.

                # Now we have gcd_series

                # Verify Publisher in database or create new
                try:
                    publisher = Publisher.objects.get(pk=gcd_series.publisher_id)
                except ObjectDoesNotExist:
                    # Need to add publisher.
                    publisher = Publisher(id=gcd_publisher.id, gcd_id=gcd_publisher.id,
                                          name=gcd_publisher.name, issue_ct=gcd_publisher.issue_count)
                    publisher.save()


                # Get or create series record
                try:
                    series = Series.objects.get(pk = gcd_series.id)
                except ObjectDoesNotExist:
                    print("Creating series:", gcd_series.id, gcd_series.name)
                    series = Series()
                    series.id = series.gcd_id = gcd_series.id
                    series.name = gcd_series.name
                    series.sort_name = gcd_series.sort_name
                    series.year_began = gcd_series.year_began
                    series.notes = gcd_series.notes
                    series.issue_count = gcd_series.issue_count
                    series.color = gcd_series.color
                    series.gcd_publisher = publisher
                    series.save()
                    print("Saved series:", series.pk)
                # ToDo: Delete genre?
                # issue.genre_id =
                issue.gcd_series = series

                gcd_issue_recs = GcdIssue.objects.filter(series_id=gcd_series.id, number=issue.number)
                series_ct = len(gcd_issue_recs)
                if series_ct == 0:
                    messages.append((issue.catalog_id, tbl_issue.name, "Series not found with this issue #"))
                    continue
                elif series_ct > 1:
                    # ToDo: Save variants in database field
                    gcd_issue = gcd_issue_recs[0]
                else:
                    # just one matching record
                    gcd_issue = gcd_issue_recs[0]

                issue.publication_date = gcd_issue.publication_date
                issue.gcd_notes = gcd_issue.notes
                issue.gcd_id = gcd_issue.id

                # Now go after cover image
                if issue.cover_image == "":
                    issue.cover_image = self.scrape_image(issue.gcd_id)

                # success! Save our issue
                issue.save()
                tbl_issue.is_done = 'Y'  # Mark record as completed
                tbl_issue.status = 'available'
                tbl_issue.save()
        context = {'errors': messages,
                   }
        return render(
            request, self.template_name, context
        )

    def scrape_image(self, gcd_issue_id):
        import urllib.request
        from bs4 import BeautifulSoup
        import re
        from PIL import Image
        from time import sleep

        print("Scraping image issue", gcd_issue_id)
        sleep(5) # Avoid Error 509 Bandwidth limitation

        # Get cover from "http://www.comics.org/issue/" + gcd_issue_id + '/cover/4/'
        with urllib.request.urlopen('http://www.comics.org/issue/' + str(gcd_issue_id) + '/cover/4/') as response:
           html = response.read()
        soup = BeautifulSoup(html)
        img = soup.find('img', 'cover_img')
        matches = re.match(r'.+src="(http.+/(\d+.jpg)).+', str(img))
        if matches is None:
            return "" # Missing cover on comics.org
        src_filename = matches.group(1)
        filename = matches.group(2)
        saved_filename = 'comix/static/bigImages/' + filename
        if not os.path.isfile(saved_filename):
            urllib.request.urlretrieve(src_filename, saved_filename)
            # Now create thumbnail
            size = (100, 156)
            thumb_filename = 'comix/static/thumbnails/' + filename
            im = Image.open(saved_filename)
            im.thumbnail(size)
            im.save(thumb_filename, "JPEG")
        return filename

