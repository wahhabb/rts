from django.shortcuts import render
from django.views.generic.list import  View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging
import os.path
from openpyxl import load_workbook
from imports.models import *
from comix.models import Publisher, Series, Issue
import datetime
from django.db.models import Q


logger = logging.getLogger(__name__)


def scrape_image(gcd_issue_id):
    import urllib.request
    from bs4 import BeautifulSoup
    import re
    from PIL import Image
    from time import sleep

    sleep(1)  # Avoid Error 509 Bandwidth limitation

    # Get cover from "http://www.comics.org/issue/" + gcd_issue_id + '/cover/4/'
    with urllib.request.urlopen('http://www.comics.org/issue/' + str(gcd_issue_id) + '/cover/4/') as response:
        html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find('img', 'cover_img')
    matches = re.match(r'.+src="(http.+/(\d+.jpg)).+', str(img))
    if matches is None:
        return ""  # Missing cover on comics.org
    src_filename = matches.group(1)
    filename = matches.group(2)
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
    return filename

# Import from tbl_comics on database
class TblComicsImportView(View):
    template_name = 'imports/imports.html'
    gcd_series_recs = None

    def get(self, request):
        wb = load_workbook(filename="data/PubFix.xlsx")
        wb.guess_types = True
        sheet = wb.active
        cells = sheet['A4':'B62']
        fixes = {}
        messages = [('Catalog No', 'Name', 'Issue', 'Year','Problem')]
        for row in cells:
            fixes[row[0].value] = row[1].value

        issues = TblComics.objects.all()

        issues = issues.filter(is_done='N')
        # issues = issues.filter(catalog_no='C20890') # for testing

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

                # Find series from title
                tmp_series_recs = GcdSeries.objects.filter(Q(name=tbl_issue.name) | Q(sort_name=tbl_issue.name))
                self.gcd_series_recs = tmp_series_recs.filter(country_id=225, year_began=tbl_issue.year)
                series_ct = len(self.gcd_series_recs)
                if series_ct == 0:
                    # failed to get match on name, drop item
                    tmp_series_recs.filter(country_id=225)
                    if len(tmp_series_recs) == 0:
                        if tbl_issue.gcd_series_id == 0:
                            messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                             "No match on name"))
                        else:
                            messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                             "Showed gcd_series_id but \nNo match on name"))
                    else:
                        if tbl_issue.gcd_series_id == 0:
                            messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                             "Match on name but not name and date"))
                        else:
                            messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                             "Showed gcd_series_id but \nNo match on name and date"))
                    continue
                elif series_ct > 1:
                    # Let's look for a unique match on title and issue #
                    gcd_issue_recs = GcdIssue.objects.filter(Q(series_id__name=tbl_issue.name) |
                                                             Q(series_id__sort_name=tbl_issue.name))
                    gcd_issue_recs = gcd_issue_recs.filter(number=issue.number)
                    issue_ct = len(gcd_issue_recs)
                    if issue_ct == 0:
                        messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                         "No match on issue name and number"))
                        continue
                    elif issue_ct == 1:
                        # assume we found our match
                        gcd_issue = gcd_issue_recs[0]
                        gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
                        gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                    else: # More than one. Try to match based on publisher
                        tmp_issue_recs = gcd_issue_recs.filter(series_id__publisher__name=tbl_issue.publisher)
                        issue_ct = len(tmp_issue_recs)
                        if issue_ct == 0:
                            messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                             "Publisher not found"))
                            continue
                        elif issue_ct > 1:
                            gcd_issue = tmp_issue_recs[0]
                            gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
                            gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                            issue.variants = ''
                            for var_issue in tmp_issue_recs:
                                issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
                            messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                             "Duplicate records for title, issue, publisher"))
                            # We are creating error message but fall through to save issue record.
                            # We won't display this issue because variants are present.
                        else: # found unique issue
                            gcd_issue = tmp_issue_recs[0]
                            gcd_series = GcdSeries.objects.get(id=tmp_issue_recs[0].series_id)
                            gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                else: # just one series_ct
                    gcd_series = self.gcd_series_recs[0]
                    gcd_publisher = GcdPublisher.objects.get(pk=gcd_series.publisher_id)
                    gcd_issue_recs = GcdIssue.objects.filter(number=issue.number, series_id=gcd_series.id)
                    if len(gcd_issue_recs) == 0:
                        messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                         "Bad issue number?"))
                        continue
                    gcd_issue = gcd_issue_recs[0]
                    # Multiple issues above are variants.
                    if len(gcd_issue_recs) > 1:
                        issue.variants = ''
                        for var_issue in gcd_issue_recs:
                            issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
                        messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                         "Variant issues"))
                        # Again, create error message but keep record

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
                    print("Saved series:", gcd_series.id, series.name)
                # ToDo: Delete genre?
                # issue.genre_id =
                issue.gcd_series = series

                gcd_issue_recs = GcdIssue.objects.filter(series_id=gcd_series.id, number=issue.number)
                series_ct = len(gcd_issue_recs)
                if series_ct == 0:
                    messages.append((issue.catalog_id, tbl_issue.name, issue.number, tbl_issue.year,
                                     "Series not found with this issue #"))
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
                    issue.cover_image = scrape_image(issue.gcd_id)

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

class Comic:
    pass


class ImportExcelView(View):
    template_name = 'imports/imports.html'
    gcd_series_recs = None

    def get(self, request):
        wb = load_workbook(filename="data/PubFix.xlsx")
        wb.guess_types = True
        sheet = wb.active
        cells = sheet['A2':'B62']
        fixes = {}
        messages = [('Catalog No', 'Name', 'Issue', 'Year','Problem')]
        for row in cells:
            fixes[row[0].value] = row[1].value

        wb = load_workbook(filename="data/RTS Master Inv Avail 2016 10 06.xlsx")
        wb.guess_types = True
        sheet = wb.active
        row = 0
        while sheet['A' + str(row + 1)].value > '':
            row += 1
            s_row = str(row)
            Comic.catalog_no = sheet['A' + s_row].value
            Comic.publisher = sheet['C' + s_row].value
            Comic.name = sheet['E' + s_row].value
            Comic.year = sheet['F' + s_row].value
            Comic.vol_no = sheet['G' + s_row].value
            Comic.issue = sheet['H' + s_row].value
            Comic.issue_text = sheet['I' + s_row].value
            Comic.grade = sheet['K' + s_row].value
            Comic.price = sheet['L' + s_row].value
            Comic.quantity = sheet['M' + s_row].value
            Comic.si = sheet['N' + s_row].value
            Comic.issue_notes = sheet['J' + s_row].value
            if Comic.issue_notes > '':
                Comic.issue_notes += ' '
            Comic.issue_notes += sheet['O' + s_row].value
            Comic.grade_notes = sheet['P' + s_row].value
            Comic.inserts = sheet['Q' + s_row].value


            try:
                c_issue = Issue.objects.get(catalog_id = Comic.catalog_no)
                c_issue.price = Comic.price
                c_issue.quantity = Comic.quantity
                c_issue.save()
                continue  # not necessary, just for clarity

            except ObjectDoesNotExist:
                # add new entry
                issue = Issue()

                # Fill in entries from input. Some may need to be fixed
                # Note: there can be multiple records for the same issue in different grades.
                issue.catalog_id = Comic.catalog_no
                issue.volume = Comic.vol_no
                issue.number = Comic.issue
                issue.issue_text = Comic.issue_text
                issue.notes = Comic.issue_notes
                issue.grade = Comic.grade
                issue.grade_notes = Comic.grade_notes
                issue.image_scanned = 0
                issue.inserts = Comic.inserts
                issue.si = Comic.si
                issue.added_date = datetime.datetime.now()
                issue.price = Comic.price
                issue.quantity = Comic.quantity
                issue.status = 'available'

                # Find series from title
                self.gcd_series_recs = GcdSeries.objects.filter(Q(name=Comic.name) | Q(sort_name=Comic.name))
                self.gcd_series_recs.filter(country_id=225, year_began=Comic.year)
                series_ct = len(self.gcd_series_recs)
                if series_ct == 0:
                    # failed to get match on name, drop item
                    messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "No match on name"))
                    continue
                elif series_ct > 1:
                    # Let's look for a unique match on title and issue #
                    gcd_issue_recs = GcdIssue.objects.filter(Q(series_id__name=Comic.name) |
                                                             Q(series_id__sort_name=Comic.name))
                    issue_ct = len(gcd_issue_recs)
                    if issue_ct == 0:
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                         "No match on issue name and number"))
                        continue
                    elif issue_ct == 1:
                        # assume we found our match
                        gcd_issue = gcd_issue_recs[0]
                        gcd_series = GcdSeries.objects.get(id=gcd_issue_recs[0].series_id)
                        gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                    else: # More than one. Try to match based on publisher
                        tmp_issue_recs = gcd_issue_recs.filter(series_id__publisher__name=Comic.publisher)
                        issue_ct = len(tmp_issue_recs)
                        if issue_ct == 0:
                            messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Publisher not found"))
                            continue
                        elif issue_ct > 1:
                            tmp_issue_recs = tmp_issue_recs.filter(variant_of_id__isnull=True) # Choose original over variants
                            if len(tmp_issue_recs) == 1:
                                gcd_issue = tmp_issue_recs[0]
                                gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
                                gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                            else:
                                messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                                 "Duplicate records for title, issue, publisher"))
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
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Bad issue number?"))
                        continue
                    gcd_issue = gcd_issue_recs[0]
                    # ToDo: Multiple issues above are variants.
                    if len(gcd_issue_recs) > 1:
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                         "Warning: has variants but added to database"))

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
                    messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Series not found with this issue #"))
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
                    issue.cover_image = scrape_image(issue.gcd_id)

                # success! Save our issue
                issue.save()
                # tbl_issue.is_done = 'Y'  # Mark record as completed
                # tbl_issue.status = 'available'
                # tbl_issue.save()

        context = {'errors': messages,
                   }
        return render(
            request, self.template_name, context
        )