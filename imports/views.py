from django.shortcuts import render
from django.views.generic.list import  View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging
import os.path
import re
from openpyxl import load_workbook, Workbook
from imports.models import *
from comix.models import Publisher, Series, Issue
from django.utils import timezone
from django.db.models import Q
from decimal import *


logger = logging.getLogger(__name__)
min_custom = 10000000


def scrape_image(gcd_issue_id):
    import urllib.request
    from bs4 import BeautifulSoup
    import re
    from PIL import Image
    from time import sleep

    sleep(2)  # Avoid Error 509 Bandwidth limitation

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



def debug(str1, str2=''):
    print(str1, str2)


def make_string(field):
    if field == None:
        return ''
    if isinstance(field, str):
        return field
    else:
        return str(field)


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

# For Tim's fixes only: remove for general loading
#         wb = load_workbook(filename="data/Year corrections.xlsx")
#         wb.guess_types = True
#         sheet = wb.active
#         cells = sheet['A2':'K205']
#         forces = {}
#         force_issues = {}
#         for row in cells:
#             if row[9].value is not None:
#                 forces[row[0].value] = row[9].value
#                 force_issues[row[0].value] = row[10].value

#   End of Tim's fixes


        # wb = load_workbook(filename="data/Master inv 33 Available Dump 2017 01 25.xlsx")
        wb = load_workbook(filename="data/errors6.xlsx")
        wb.guess_types = True
        sheet = wb.active
        row = 1
        while make_string(sheet['A' + str(row + 1)].value) > '':
            row += 1
            # if row > 6:
            #     break   # ToDo: remove, just for testing
            s_row = str(row)

            Comic.catalog_no = make_string(sheet['A' + s_row].value)

            Comic.name = str(sheet['B' + s_row].value)
            ls_pos = Comic.name.find(' L.S.')
            if ls_pos > 0:
                Comic.name = Comic.name[:ls_pos] # remove L.S. from name
            Comic.sort_name = make_string(sheet['C' + s_row].value)
            Comic.publisher = make_string(sheet['D' + s_row].value)

            t_year = sheet['E' + s_row].value
            if t_year == None:
                Comic.year = 0
            else:
                Comic.year = int(t_year)
            Comic.vol_no = make_string(sheet['F' + s_row].value)
            Comic.issue = make_string(sheet['G' + s_row].value)
            Comic.issue_text = make_string(sheet['H' + s_row].value)
            Comic.edition = make_string(sheet['I' + s_row].value)
            Comic.grade = make_string(sheet['J' + s_row].value)
            Comic.price = Decimal(sheet['K' + s_row].value)
            Comic.quantity = int(sheet['L' + s_row].value)
            Comic.scarcity_notes = make_string(sheet['M' + s_row].value)
            Comic.issue_notes = make_string(sheet['N' + s_row].value)
            Comic.grade_notes = make_string(sheet['O' + s_row].value)
            Comic.inserts = make_string(sheet['P' + s_row].value)
            Comic.indicia_date = make_string(sheet['Q' + s_row].value)
            Comic.not_in_gcd = make_string(sheet['T' + s_row].value)
            Comic.numerical_grade = make_string(sheet['U' + s_row].value)
            found_series = make_string(sheet['R' + s_row].value)
            found_issue = make_string(sheet['S' + s_row].value)

            if found_issue is not None and found_issue != '':
                c_issue = Issue.objects.filter(catalog_id=Comic.catalog_no)

                if len(c_issue) == 0:
                    issue = Issue()
                else:
                    issue = c_issue[0]

                gcd_issue = GcdIssue.objects.get(id=int(found_issue))
                gcd_series = GcdSeries.objects.get(id=int(found_series))
                if int(found_series) != gcd_issue.series_id:
                    messages.append((Comic.catalog_no, Comic.name, Comic.vol_no, Comic.issue, Comic.year,
                                     "Inconsistent Series & Issue"))
                    continue

                gcd_publisher = GcdPublisher.objects.get(id = gcd_series.publisher_id)
                issue.publication_date = gcd_issue.publication_date
                issue.gcd_notes = gcd_issue.notes
                # Verify Publisher in database or create new
                try:
                    # debug('Checking Publisher:', gcd_publisher.name)
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
                    series.sort_name = Comic.sort_name
                    series.year_began = gcd_series.year_began
                    series.notes = gcd_series.notes
                    series.issue_count = gcd_series.issue_count
                    series.color = gcd_series.color
                    series.gcd_publisher = publisher

                    series.save()
                    print("Saved series:", series.pk)

                issue.gcd_series = series
                issue.gcd_id = gcd_issue.id
                if found_series == '30403':     # Classics Illustrated
                    hrn = issue.edition[5:]
                    hrn = hrn[:len(hrn)-1]
                    try:
                        issue.hrn_number = int(hrn)
                    except:
                        hrn = hrn # no-op
            # Now go after cover image
            issue.cover_image = ""     # Temporary: ToDo: Remove
            if issue.cover_image == "":
                issue.cover_image = scrape_image(issue.gcd_id)

            else:
                c_issue = Issue.objects.filter(catalog_id=Comic.catalog_no)

                if len(c_issue) == 0:
                    # Add as not on GCD
                    issue = Issue()
                    issue.in_gcd_flag = False
                    iid = Issue.objects.latest('gcd_id').gcd_id + 1
                    if iid < min_custom:
                        iid = min_custom
                    issue.id = issue.gcd_id = iid
                    try:
                        publisher = Publisher.objects.get(name=Comic.publisher)
                    except Publisher.DoesNotExist:
                        publisher = Publisher()
                        pid = Publisher.objects.latest('gcd_id').gcd_id + 1
                        if pid < min_custom:
                            pid = min_custom
                        publisher.id = publisher.gcd_id = pid
                        publisher.in_gcd_flag = False
                        publisher.issue_ct = 0  # ignore for not on GCD
                        publisher.name = Comic.publisher
                        debug('Adding publisher not in GCD:', publisher.name)
                        publisher.save()
                    try:
                       series = Series.objects.get(name=Comic.name, year_began=Comic.year, in_gcd_flag=False)
                    except Series.DoesNotExist:
                        series = Series()
                        series.in_gcd_flag = False
                        sid = Series.objects.latest('gcd_id').gcd_id + 1
                        if sid < min_custom:
                            sid = min_custom
                        series.id = series.gcd_id = sid
                        series.name = Comic.name
                        series.sort_name = Comic.sort_name
                        series.year_began = Comic.year
                        series.gcd_publisher = publisher
                        series.issue_count = 0      # ignore for not on GCD
                        series.save()
                        print("Saved series:", series.pk)
                    issue.gcd_series = series

                else:
                    issue = c_issue[0]
                    # series = issue.gcd_series
                    # publisher = series.gcd_publisher
                    # gcd_issue = GcdIssue.objects.get(id=issue.gcd_id)
                    # gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
                    # gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)

            # print('Trying:', Comic.catalog_no)
            issue.variants = ""
            issue.catalog_id = Comic.catalog_no
            issue.volume = Comic.vol_no
            issue.show_number = Comic.issue
            try:
                issue.number = int(Comic.issue)
            except ValueError:
                issue.number = 0
            issue.issue_text = Comic.issue_text
            issue.edition = Comic.edition
            issue.grade = Comic.grade
            issue.grade_notes = Comic.grade_notes
            issue.price = Comic.price
            issue.quantity = Comic.quantity
            issue.indicia_date = Comic.indicia_date
            issue.image_scanned = 0
            issue.inserts = Comic.inserts
            issue.scarcity_notes = Comic.scarcity_notes
            issue.notes = Comic.issue_notes
            issue.status = 'available'
            issue.numerical_grade = Comic.numerical_grade
            if issue.numerical_grade == '':
                issue.numerical_grade = 0

            sheet['R' + s_row] = issue.gcd_series_id
            sheet['S' + s_row] = issue.gcd_id

            #   sheet['T' + s_row] = issue.gcd_series.gcd_publisher_id
            #     sheet['U' + s_row] = c_issue.gcd_series.year_began
            # sheet['W' + s_row] = series.name
            # sheet['X' + s_row] = gcd_series.name
            # sheet['Y' + s_row] = publisher.name
            # sheet['Z' + s_row] = gcd_publisher.name
            # sheet['AA' + s_row] = series.year_began
            # sheet['AB' + s_row] = gcd_series.year_began
            # sheet['AC' + s_row] = issue.volume
            # sheet['AD' + s_row] = gcd_issue.volume
            # sheet['AE' + s_row] = issue.show_number
            # sheet['AF' + s_row] = gcd_issue.number
            # sheet['AG' + s_row] = gcd_issue.variant_name
            # sheet['AH' + s_row] = issue.indicia_date
            # sheet['AI' + s_row] = gcd_issue.publication_date

            # print('.', end='')
            issue.save()
            continue



            #
            # # issue.cover_image = ''              # Remove if not needed
            # found_series = forces[issue.catalog_id]
            # found_issue = force_issues[issue.catalog_id]
            #
            # if found_issue is None or found_issue == "":
            #     continue
            # if found_issue is not None and found_issue != "":
            #     gcd_issue = GcdIssue.objects.get(id=found_issue)
            #     gcd_series = GcdSeries.objects.get(id=found_series)
            # else:
            #     try:
            #         gcd_series = GcdSeries.objects.get(id = found_series)
            #     except GcdSeries.DoesNotExist:
            #         messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                          "Series # not on GCD"))
            #         continue
            #     try:
            #         gcd_issue = GcdIssue.objects.get(series_id=gcd_series.id, number=issue.number,
            #                                          volume=issue.volume)
            #     except GcdIssue.DoesNotExist:
            #         try:
            #             gcd_issue = GcdIssue.objects.get(series_id=gcd_series.id, number=issue.number)
            #         except GcdIssue.DoesNotExist:
            #             messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                              "No match Volume & Issue #"))
            #             continue
            #         except MultipleObjectsReturned:
            #             tmp_issue_recs = GcdIssue.objects.filter(series_id=gcd_series.id, number=issue.number)
            #             issue_ct = len(tmp_issue_recs)
            #             debug('variants count:', str(issue_ct))
            #             gcd_issue = tmp_issue_recs[0]
            #             issue.variants = ''
            #             for var_issue in tmp_issue_recs:
            #                 issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
            #                 debug('issue.variants:', issue.variants)
            #             messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                              "Duplicate records for title, issue, publisher"))
            #             # We are creating error message but fall through to save issue record.
            #             # We won't display this issue because variants are present.
            #     except MultipleObjectsReturned:
            #         tmp_issue_recs = GcdIssue.objects.filter(series_id=gcd_series.id, number=issue.number,
            #                                                  volume=issue.volume)
            #         issue_ct = len(tmp_issue_recs)
            #         debug('variants count:', str(issue_ct))
            #         gcd_issue = tmp_issue_recs[0]
            #         issue.variants = ''
            #         for var_issue in tmp_issue_recs:
            #             issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
            #             debug('issue.variants:', issue.variants)
            #         messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                          "Duplicate records for title, volume, issue, publisher"))
            #         # We are creating error message but fall through to save issue record.
            #         # We won't display this issue because variants are present.
            #
            # # if gcd_issue.number == '???':
            # #     messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            # #                      "Non-numeric Issue #"))
            # #     continue
            # gcd_publisher = GcdPublisher.objects.get(id = gcd_series.publisher_id)
            # issue.publication_date = gcd_issue.publication_date
            # issue.gcd_notes = gcd_issue.notes
            # # Verify Publisher in database or create new
            # try:
            #     # debug('Checking Publisher:', gcd_publisher.name)
            #     publisher = Publisher.objects.get(pk=gcd_series.publisher_id)
            # except ObjectDoesNotExist:
            #     # Need to add publisher.
            #     publisher = Publisher(id=gcd_publisher.id, gcd_id=gcd_publisher.id,
            #                           name=gcd_publisher.name, issue_ct=gcd_publisher.issue_count)
            #     publisher.save()
            # # Get or create series record
            # try:
            #     series = Series.objects.get(pk = gcd_series.id)
            # except ObjectDoesNotExist:
            #     print("Creating series:", gcd_series.id, gcd_series.name)
            #     series = Series()
            #     series.id = series.gcd_id = gcd_series.id
            #     series.name = gcd_series.name
            #     series.sort_name = Comic.sort_name
            #     series.year_began = gcd_series.year_began
            #     series.notes = gcd_series.notes
            #     series.issue_count = gcd_series.issue_count
            #     series.color = gcd_series.color
            #     series.gcd_publisher = publisher
            #     series.save()
            #     print("Saved series:", series.pk)
            # issue.gcd_series = series
            # issue.gcd_id = gcd_issue.id
            # # Now go after cover image
            # if issue.cover_image == "":
            #     issue.cover_image = scrape_image(issue.gcd_id)
            #
            # # success! Save our issue
            # issue.save()
            # debug("Issue saved", str(issue))
            # continue
            #   # End of Tim's fixes
            #   #
            #   # Temporary fix ToDo: Remove
            #
            # gcd_series = GcdSeries.objects.get(id=found_series)
            # gcd_issue_recs = GcdIssue.objects.filter(series=gcd_series, number=Comic.issue, volume=Comic.vol_no)
            # issue_ct = len(gcd_issue_recs)
            #
            # if issue_ct > 1:
            #     messages.append((Comic.catalog_no, Comic.name, Comic.issue, Comic.year,
            #                      "Multiple matches: variants?"))
            #     continue
            # if issue_ct == 1:
            #     if gcd_issue_recs[0].id != int(found_issue):
            #         gcd_issue = gcd_issue_recs[0]
            #         issue = Issue.objects.get(catalog_id=Comic.catalog_no)
            #         debug('Fixing item:', issue)
            #         issue.gcd_id = gcd_issue.id
            #
            #         issue.publication_date = gcd_issue.publication_date
            #         issue.gcd_notes = gcd_issue.notes
            #         issue.cover_image = scrape_image(issue.gcd_id)
            #         # success! Save our issue
            #         issue.save()
            #         debug("Issue saved", str(issue))
            #         continue
            #     continue
            # #   End temporary fix
            # # if issue_ct == 0:
            #     #     messages.append((Comic.catalog_no, Comic.name, Comic.issue, Comic.year,            try:
            #     #                      "No match on issue name and number"))                c_issue = Issue.objects.get(catalog_id = Comic.catalog_no)
            #     #     continue                # ToDo: restore next three lines for production
            #     #     c_issue.price = Comic.price
            #     #     c_issue.quantity = Comic.quantity
            #     #     c_issue.grade = Comic.grade
            #     #     c_issue.grade_notes = Comic.grade_notes
            #     #     c_series = c_issue.gcd_series
            #     #     c_series.sort_name = Comic.sort_name
            #     #     sheet['R' + s_row] = c_issue.gcd_id
            #     #     sheet['S' + s_row] = c_issue.gcd_series_id
            #     #     sheet['T' + s_row] = c_issue.gcd_series.gcd_publisher_id
            #     #     sheet['U' + s_row] = c_issue.gcd_series.year_began
            #     #     c_series.save()
            #     #     c_issue.save()
            #     #     continue  # not necessary, just for clarity
            #     #
            #     # except ObjectDoesNotExist:
            #     # add new entry
            #     # debug('creating issue:', Comic.catalog_no)
            #
            #     # issue = Issue()
            #     issue = Issue.objects.get(catalog_id=Comic.catalog_no)      # Remove after fixes
            #
            #     # Fill in entries from input. Some may need to be fixed
            #     # Note: there can be multiple records for the same issue in different grades.
            #     issue.catalog_id = Comic.catalog_no
            #     issue.volume = Comic.vol_no
            #     issue.number = Comic.issue
            #     issue.issue_text = Comic.issue_text
            #     issue.notes = Comic.issue_notes
            #     issue.grade = Comic.grade
            #     issue.grade_notes = Comic.grade_notes
            #     issue.image_scanned = 0
            #     issue.inserts = Comic.inserts
            #     issue.si = Comic.si
            #     issue.added_date = timezone.now()
            #     issue.price = Comic.price
            #     issue.quantity = Comic.quantity
            #     issue.status = 'available'
            #
            #     # Find series from title and year begun
            #     tmp_series_recs = GcdSeries.objects.filter(Q(name=Comic.name) | Q(sort_name=Comic.name))
            #     self.gcd_series_recs = tmp_series_recs.filter(country_id=225, year_began=Comic.year)
            #     series_ct = len(self.gcd_series_recs)
            #     # debug('series_ct', str(series_ct))
            #     if series_ct == 0:  # Try matching without punctuation
            #         old_name = Comic.name
            #         new_name = old_name.replace("&", "and")
            #         new_name = re.sub(r'[-"\',.:! ]', '', new_name)
            #         tmp2_series_recs = GcdSeries.objects.filter(text_name=new_name)
            #         self.gcd_series_recs = tmp2_series_recs.filter(country_id=225, year_began=Comic.year)
            #         series_ct = len(self.gcd_series_recs)
            #         if series_ct == 0:
            #             # No luck, Check for year before or after
            #             self.gcd_series_recs = tmp2_series_recs.filter(country_id=225, year_began=Comic.year + 1)
            #             series_ct = len(self.gcd_series_recs)
            #             if series_ct == 0:
            #                 self.gcd_series_recs = tmp2_series_recs.filter(country_id=225, year_began=Comic.year + 1)
            #                 series_ct = len(self.gcd_series_recs)
            #                 if series_ct == 0:
            #                     # see if unique match ignoring year
            #                     self.gcd_series_recs = tmp2_series_recs.filter(country_id=225)
            #                     series_ct = len(self.gcd_series_recs)
            #                     if series_ct != 1:
            #                         # failed to get match on name, drop item
            #                         messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                                          "No match on name"))
            #                         continue
            #                         # else:
            #                         #     print('Got unique on', Comic.catalog_no, Comic.name, '#' + Comic.issue)
            #     if series_ct > 1:
            #         # Let's look for a unique match on title and issue #
            #         gcd_issue_recs = GcdIssue.objects.filter(Q(series_id__name=Comic.name) |
            #                                                  Q(series_id__sort_name=Comic.name))
            #         gcd_issue_recs = gcd_issue_recs.filter(number=Comic.issue, volume=Comic.vol_no)
            #         issue_ct = len(gcd_issue_recs)
            #         if issue_ct == 0:
            #             messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                              "No match on issue name and number"))
            #             continue
            #         elif issue_ct == 1:
            #             # assume we found our match
            #             gcd_issue = gcd_issue_recs[0]
            #             gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
            #             gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
            #         else: # More than one. Try to match based on publisher
            #             tmp_issue_recs = gcd_issue_recs.filter(series_id__publisher__name=Comic.publisher)
            #             issue_ct = len(tmp_issue_recs)
            #             if issue_ct == 0:
            #                 messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Publisher not found"))
            #                 continue
            #             elif issue_ct > 1: # have variants
            #                 debug('variants count:', str(issue_ct))
            #                 gcd_issue = tmp_issue_recs[0]
            #                 gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
            #                 gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
            #                 issue.variants = ''
            #                 for var_issue in tmp_issue_recs:
            #                     issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
            #                     debug('issue.variants:', issue.variants)
            #                 messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                                  "Duplicate records for title, issue, publisher"))
            #                 # We are creating error message but fall through to save issue record.
            #                 # We won't display this issue because variants are present.
            #             else:   # found our match
            #                 gcd_issue = tmp_issue_recs[0]
            #                 gcd_series = GcdSeries.objects.get(id=tmp_issue_recs[0].series_id)
            #                 gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
            #     else: # just one series_ct
            #         gcd_series = self.gcd_series_recs[0]
            #         gcd_publisher = GcdPublisher.objects.get(pk=gcd_series.publisher_id)
            #         gcd_issue_recs = GcdIssue.objects.filter(number=issue.number,
            #                                                  series_id=gcd_series.id, volume=Comic.vol_no)
            #         if len(gcd_issue_recs) == 0:
            #             gcd_issue_recs = GcdIssue.objects.filter(number=issue.number, series_id=gcd_series.id)
            #             if len(gcd_issue_recs) == 0:
            #                 a1 = issue.number
            #                 a2 = gcd_series.id
            #                 messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Bad issue number?"))
            #                 continue
            #         gcd_issue = gcd_issue_recs[0]
            #         # Multiple issues above are variants.
            #         if len(gcd_issue_recs) > 1:
            #             debug('variants count:', str(len(gcd_issue_recs)))
            #             issue.variants = ''
            #             for var_issue in gcd_issue_recs:
            #                 issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
            #                 debug('issue.variants:', issue.variants)
            #             messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                              "Variant issues"))
            #             # Again, create error message but keep record
            #
            #     # Now we have gcd_series
            #
            #     # Verify Publisher in database or create new
            #     try:
            #         # debug('Checking Publisher:', gcd_publisher.name)
            #         publisher = Publisher.objects.get(pk=gcd_series.publisher_id)
            #     except ObjectDoesNotExist:
            #         # Need to add publisher.
            #         publisher = Publisher(id=gcd_publisher.id, gcd_id=gcd_publisher.id,
            #                               name=gcd_publisher.name, issue_ct=gcd_publisher.issue_count)
            #         publisher.save()
            #
            #
            #     # Get or create series record
            #     try:
            #         series = Series.objects.get(pk = gcd_series.id)
            #     except ObjectDoesNotExist:
            #         print("Creating series:", gcd_series.id, gcd_series.name)
            #         series = Series()
            #         series.id = series.gcd_id = gcd_series.id
            #         series.name = gcd_series.name
            #         series.sort_name = Comic.sort_name
            #         series.year_began = gcd_series.year_began
            #         series.notes = gcd_series.notes
            #         series.issue_count = gcd_series.issue_count
            #         series.color = gcd_series.color
            #         series.gcd_publisher = publisher
            #         series.save()
            #         print("Saved series:", series.pk)
            #     # ToDo: Set genre
            #     # issue.genre_id =
            #     issue.gcd_series = series
            #     issue.publication_date = gcd_issue.publication_date
            #     issue.gcd_notes = gcd_issue.notes
            #     issue.gcd_id = gcd_issue.id
            #
            #     # Now go after cover image
            #     if issue.cover_image == "":
            #         issue.cover_image = scrape_image(issue.gcd_id)
            #
            #     # success! Save our issue
            #     issue.save()
            #     debug("Issue saved", str(issue))

        # wb.save(filename='data/Updated Inv 3 2017 01 25.xlsx')
        context = {'errors': messages,
                   }
        return render(
            request, self.template_name, context
        )


class FixesExcelView(View):
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

# For Tim's fixes only: remove for general loading
#         wb = load_workbook(filename="data/Year corrections.xlsx")
#         wb.guess_types = True
#         sheet = wb.active
#         cells = sheet['A2':'J205']
#         forces = {}
#         for row in cells:
#             if row[9].value is not None:
#                 forces[row[0].value] = row[9].value
#   End of Tim's fixes

        wb = load_workbook(filename="data/Error Corrections 2017 01 21.xlsx")
        wb.guess_types = True
        sheet = wb.active
        row = 1
        while make_string(sheet['A' + str(row + 1)].value) > '':
            row += 1
            # if row > 4:
            #     break   # ToDo: remove, just for testing
            s_row = str(row)
            not_in_gcd = make_string(sheet['T' + s_row].value)
            if not_in_gcd:
                continue    # deal later

            Comic.catalog_no = make_string(sheet['A' + s_row].value)
            Comic.name = str(sheet['B' + s_row].value)
            ls_pos = Comic.name.find(' L.S.')
            if ls_pos > 0:
                Comic.name = Comic.name[:ls_pos] # remove L.S. from name
            Comic.sort_name = sheet['C' + s_row].value
            Comic.publisher = sheet['D' + s_row].value

            t_year = sheet['E' + s_row].value
            if t_year == None:
                Comic.year = 0
            else:
                Comic.year = int(t_year)
            Comic.vol_no = make_string(sheet['F' + s_row].value)
            Comic.issue = make_string(sheet['G' + s_row].value)
            Comic.issue_text = make_string(sheet['H' + s_row].value)
            # Comic.issue_notes = make_string(sheet['J' + s_row].value)
            Comic.edition = make_string(sheet['I' + s_row].value)
            Comic.grade = make_string(sheet['J' + s_row].value)
            Comic.price = Decimal(sheet['K' + s_row].value)
            Comic.quantity = int(sheet['L' + s_row].value)
            Comic.si = make_string(sheet['M' + s_row].value)
            Comic.issue_notes = make_string(sheet['N' + s_row].value)
            Comic.grade_notes = make_string(sheet['O' + s_row].value)
            Comic.inserts = make_string(sheet['P' + s_row].value)
            Comic.indicia_date = make_string(sheet['Q' + s_row].value)
            found_series = make_string(sheet['R' + s_row].value)
            found_issue = make_string(sheet['S' + s_row].value)
            if found_series == '':
                continue






                # wb = load_workbook(filename="data/Updated Inv 2016 12 20.xlsx")

                # wb = load_workbook(filename="data/RTS Master Inv 2016 12 20.xlsx")
                # wb.guess_types = True
                # sheet = wb.active
                # row = 1
                # while make_string(sheet['A' + str(row + 1)].value) > '':
                #     row += 1
                #     # if row > 6:
                #     #     break   # ToDo: remove, just for testing
                #     s_row = str(row)
                #
                #     Comic.catalog_no = make_string(sheet['A' + s_row].value)
                #     Comic.name = str(sheet['E' + s_row].value)
                #     ls_pos = Comic.name.find(' L.S.')
                #     if ls_pos > 0:
                #         Comic.name = Comic.name[:ls_pos] # remove L.S. from name
                #     Comic.sort_name = sheet['D' + s_row].value
                #     Comic.publisher = sheet['C' + s_row].value
                #
                #     t_year = sheet['F' + s_row].value
                #     if t_year == None:
                #         Comic.year = 0
                #     else:
                #         Comic.year = int(t_year)
                #     Comic.vol_no = make_string(sheet['G' + s_row].value)
                #     Comic.issue = make_string(sheet['H' + s_row].value)
                #     Comic.issue_text = make_string(sheet['I' + s_row].value)
                #     Comic.edition = make_string(sheet['J' + s_row].value)
                #     Comic.grade = make_string(sheet['K' + s_row].value)
                #     Comic.price = Decimal(sheet['L' + s_row].value)
                #     Comic.quantity = int(sheet['M' + s_row].value)
                #     Comic.si = make_string(sheet['N' + s_row].value)
                #     Comic.issue_notes = make_string(sheet['O' + s_row].value)
                #     Comic.grade_notes = make_string(sheet['P' + s_row].value)
                #     Comic.inserts = make_string(sheet['Q' + s_row].value)
                #     # Comic.indicia_date = make_string(sheet['Q' + s_row].value)


            #            Tim's fixes below

            # Tim's fixes only
            # For Tim's fixes only: remove for general loading
            c_issue = Issue.objects.filter(catalog_id=Comic.catalog_no)
            if len(c_issue) == 0:
                issue = Issue()
            else:
                issue = c_issue[0]
            # print('Trying:', Comic.catalog_no)
            # issue.variants = ""
            issue.catalog_id = Comic.catalog_no
            issue.volume = Comic.vol_no
            issue.show_number = Comic.issue
            try:
                issue.number = int(Comic.issue)
            except ValueError:
                issue.number = 0
            issue.issue_text = Comic.issue_text
            issue.notes = Comic.issue_notes
            issue.grade = Comic.grade
            issue.grade_notes = Comic.grade_notes
            issue.image_scanned = 0
            issue.inserts = Comic.inserts
            issue.si = Comic.si
            issue.added_date = timezone.now()
            issue.price = Comic.price
            issue.quantity = Comic.quantity
            issue.status = 'available'
            issue.cover_image = ''      # Remove if not needed

            if found_issue > "":
                gcd_issue = GcdIssue.objects.get(id=found_issue)
                gcd_series = GcdSeries.objects.get(id=found_series)
            else:
                try:
                    gcd_series = GcdSeries.objects.get(id = found_series)
                except GcdSeries.DoesNotExist:
                    messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                     "Series # not on GCD"))
                    continue
                try:
                    gcd_issue = GcdIssue.objects.get(series_id=gcd_series.id, number=issue.number,
                                                     volume=issue.volume)
                except GcdIssue.DoesNotExist:
                    try:
                        gcd_issue = GcdIssue.objects.get(series_id=gcd_series.id, number=issue.number)
                    except GcdIssue.DoesNotExist:
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                         "No match Volume & Issue #"))
                        continue
                    except MultipleObjectsReturned:
                        tmp_issue_recs = GcdIssue.objects.filter(series_id=gcd_series.id, number=issue.number)
                        issue_ct = len(tmp_issue_recs)
                        debug('variants count:', str(issue_ct))
                        gcd_issue = tmp_issue_recs[0]
                        issue.variants = ''
                        for var_issue in tmp_issue_recs:
                            issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
                            debug('issue.variants:', issue.variants)
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                         "Duplicate records for title, issue, publisher"))
                        # We are creating error message but fall through to save issue record.
                        # We won't display this issue because variants are present.
                except MultipleObjectsReturned:
                    tmp_issue_recs = GcdIssue.objects.filter(series_id=gcd_series.id, number=issue.number,
                                                             volume=issue.volume)
                    issue_ct = len(tmp_issue_recs)
                    debug('variants count:', str(issue_ct))
                    gcd_issue = tmp_issue_recs[0]
                    issue.variants = ''
                    for var_issue in tmp_issue_recs:
                        issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
                        debug('issue.variants:', issue.variants)
                    messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                     "Duplicate records for title, volume, issue, publisher"))
                    # We are creating error message but fall through to save issue record.
                    # We won't display this issue because variants are present.

            # if gcd_issue.number == '???':
            #     messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
            #                      "Non-numeric Issue #"))
            #     continue
            gcd_publisher = GcdPublisher.objects.get(id = gcd_series.publisher_id)
            issue.publication_date = gcd_issue.publication_date
            issue.gcd_notes = gcd_issue.notes
            # Verify Publisher in database or create new
            try:
                # debug('Checking Publisher:', gcd_publisher.name)
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
                series.sort_name = Comic.sort_name
                series.year_began = gcd_series.year_began
                series.notes = gcd_series.notes
                series.issue_count = gcd_series.issue_count
                series.color = gcd_series.color
                series.gcd_publisher = publisher
                series.save()
                print("Saved series:", series.pk)
            issue.gcd_series = series
            issue.gcd_id = gcd_issue.id
            # Now go after cover image
            if issue.cover_image == "":
                issue.cover_image = scrape_image(issue.gcd_id)

            # success! Save our issue
            issue.save()
            debug("Issue saved", str(issue))
            continue
            #   End of Tim's fixes

            #   Temporary fix ToDo: Remove

            gcd_series = GcdSeries.objects.get(id=found_series)
            gcd_issue_recs = GcdIssue.objects.filter(series=gcd_series, number=Comic.issue, volume=Comic.vol_no)
            issue_ct = len(gcd_issue_recs)

            if issue_ct > 1:
                messages.append((Comic.catalog_no, Comic.name, Comic.issue, Comic.year,
                                 "Multiple matches: variants?"))
                continue
            if issue_ct == 1:
                if gcd_issue_recs[0].id != int(found_issue):
                    gcd_issue = gcd_issue_recs[0]
                    issue = Issue.objects.get(catalog_id=Comic.catalog_no)
                    debug('Fixing item:', issue)
                    issue.gcd_id = gcd_issue.id

                    issue.publication_date = gcd_issue.publication_date
                    issue.gcd_notes = gcd_issue.notes
                    issue.cover_image = scrape_image(issue.gcd_id)
                    # success! Save our issue
                    issue.save()
                    debug("Issue saved", str(issue))
                    continue
                continue
            #   End temporary fix
            if issue_ct == 0:
                #     messages.append((Comic.catalog_no, Comic.name, Comic.issue, Comic.year,            try:
                #                      "No match on issue name and number"))                c_issue = Issue.objects.get(catalog_id = Comic.catalog_no)
                #     continue                # ToDo: restore next three lines for production
                #     c_issue.price = Comic.price
                #     c_issue.quantity = Comic.quantity
                #     c_issue.grade = Comic.grade
                #     c_issue.grade_notes = Comic.grade_notes
                #     c_series = c_issue.gcd_series
                #     c_series.sort_name = Comic.sort_name
                #     sheet['R' + s_row] = c_issue.gcd_id
                #     sheet['S' + s_row] = c_issue.gcd_series_id
                #     sheet['T' + s_row] = c_issue.gcd_series.gcd_publisher_id
                #     sheet['U' + s_row] = c_issue.gcd_series.year_began
                #     c_series.save()
                #     c_issue.save()
                #     continue  # not necessary, just for clarity
                #
                # except ObjectDoesNotExist:
                # add new entry
                # debug('creating issue:', Comic.catalog_no)
                # issue = Issue()
                issue = Issue.objects.get(catalog_id=Comic.catalog_no)      # Remove after fixes

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
                issue.added_date = timezone.now()
                issue.price = Comic.price
                issue.quantity = Comic.quantity
                issue.status = 'available'

                # Find series from title and year begun
                tmp_series_recs = GcdSeries.objects.filter(Q(name=Comic.name) | Q(sort_name=Comic.name))
                self.gcd_series_recs = tmp_series_recs.filter(country_id=225, year_began=Comic.year)
                series_ct = len(self.gcd_series_recs)
                # debug('series_ct', str(series_ct))
                if series_ct == 0:  # Try matching without punctuation
                    old_name = Comic.name
                    new_name = old_name.replace("&", "and")
                    new_name = re.sub(r'[-"\',.:! ]', '', new_name)
                    tmp2_series_recs = GcdSeries.objects.filter(text_name=new_name)
                    self.gcd_series_recs = tmp2_series_recs.filter(country_id=225, year_began=Comic.year)
                    series_ct = len(self.gcd_series_recs)
                    if series_ct == 0:
                        # No luck, Check for year before or after
                        self.gcd_series_recs = tmp2_series_recs.filter(country_id=225, year_began=Comic.year + 1)
                        series_ct = len(self.gcd_series_recs)
                        if series_ct == 0:
                            self.gcd_series_recs = tmp2_series_recs.filter(country_id=225, year_began=Comic.year + 1)
                            series_ct = len(self.gcd_series_recs)
                            if series_ct == 0:
                                # see if unique match ignoring year
                                self.gcd_series_recs = tmp2_series_recs.filter(country_id=225)
                                series_ct = len(self.gcd_series_recs)
                                if series_ct != 1:
                                    # failed to get match on name, drop item
                                    messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                                     "No match on name"))
                                    continue
                                    # else:
                                    #     print('Got unique on', Comic.catalog_no, Comic.name, '#' + Comic.issue)
                if series_ct > 1:
                    # Let's look for a unique match on title and issue #
                    gcd_issue_recs = GcdIssue.objects.filter(Q(series_id__name=Comic.name) |
                                                             Q(series_id__sort_name=Comic.name))
                    gcd_issue_recs = gcd_issue_recs.filter(number=Comic.issue, volume=Comic.vol_no)
                    issue_ct = len(gcd_issue_recs)
                    if issue_ct == 0:
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                         "No match on issue name and number"))
                        continue
                    elif issue_ct == 1:
                        # assume we found our match
                        gcd_issue = gcd_issue_recs[0]
                        gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
                        gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                    else: # More than one. Try to match based on publisher
                        tmp_issue_recs = gcd_issue_recs.filter(series_id__publisher__name=Comic.publisher)
                        issue_ct = len(tmp_issue_recs)
                        if issue_ct == 0:
                            messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Publisher not found"))
                            continue
                        elif issue_ct > 1: # have variants
                            debug('variants count:', str(issue_ct))
                            gcd_issue = tmp_issue_recs[0]
                            gcd_series = GcdSeries.objects.get(id=gcd_issue.series_id)
                            gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                            issue.variants = ''
                            for var_issue in tmp_issue_recs:
                                issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
                                debug('issue.variants:', issue.variants)
                            messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                             "Duplicate records for title, issue, publisher"))
                            # We are creating error message but fall through to save issue record.
                            # We won't display this issue because variants are present.
                        else:   # found our match
                            gcd_issue = tmp_issue_recs[0]
                            gcd_series = GcdSeries.objects.get(id=tmp_issue_recs[0].series_id)
                            gcd_publisher = GcdPublisher.objects.get(id=gcd_series.publisher_id)
                else: # just one series_ct
                    gcd_series = self.gcd_series_recs[0]
                    gcd_publisher = GcdPublisher.objects.get(pk=gcd_series.publisher_id)
                    gcd_issue_recs = GcdIssue.objects.filter(number=issue.number,
                                                             series_id=gcd_series.id, volume=Comic.vol_no)
                    if len(gcd_issue_recs) == 0:
                        gcd_issue_recs = GcdIssue.objects.filter(number=issue.number, series_id=gcd_series.id)
                        if len(gcd_issue_recs) == 0:
                            a1 = issue.number
                            a2 = gcd_series.id
                            messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year, "Bad issue number?"))
                            continue
                    gcd_issue = gcd_issue_recs[0]
                    # Multiple issues above are variants.
                    if len(gcd_issue_recs) > 1:
                        debug('variants count:', str(len(gcd_issue_recs)))
                        issue.variants = ''
                        for var_issue in gcd_issue_recs:
                            issue.variants += str(var_issue.id) + ',' + str(var_issue.series_id) + ','
                            debug('issue.variants:', issue.variants)
                        messages.append((issue.catalog_id, Comic.name, issue.number, Comic.year,
                                         "Variant issues"))
                        # Again, create error message but keep record

                # Now we have gcd_series

                # Verify Publisher in database or create new
                try:
                    # debug('Checking Publisher:', gcd_publisher.name)
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
                    series.sort_name = Comic.sort_name
                    series.year_began = gcd_series.year_began
                    series.notes = gcd_series.notes
                    series.issue_count = gcd_series.issue_count
                    series.color = gcd_series.color
                    series.gcd_publisher = publisher
                    series.save()
                    print("Saved series:", series.pk)
                # ToDo: Set genre
                # issue.genre_id =
                issue.gcd_series = series
                issue.publication_date = gcd_issue.publication_date
                issue.gcd_notes = gcd_issue.notes
                issue.gcd_id = gcd_issue.id

                # Now go after cover image
                if issue.cover_image == "":
                    issue.cover_image = scrape_image(issue.gcd_id)

                # success! Save our issue
                issue.save()
                debug("Issue saved", str(issue))

        wb.save(filename='data/Updated Inv 2016 12 20.xlsx')
        context = {'errors': messages,
                   }
        return render(
            request, self.template_name, context
        )

class VariantImportExcelView(View):
    template_name = 'imports/imports.html'
    gcd_series_recs = None

    def get(self, request):
        wb = load_workbook(filename="data/PubFix.xlsx")
        wb.guess_types = True
        sheet = wb.active
        cells = sheet['A2':'B62']
        fixes = {}
        messages = [('Catalog No', 'Name', 'Volume', 'Issue', 'Year', 'Problem')]
        for row in cells:
            fixes[row[0].value] = row[1].value

        wb = load_workbook(filename="data/RTS Master Inv 2016 12 20.xlsx")
        wb.guess_types = True
        sheet = wb.active
        row = 1
        while make_string(sheet['A' + str(row + 1)].value) > '':
            row += 1
            # if row > 6:
            #     break   # ToDo: remove, just for testing
            s_row = str(row)
            Comic.catalog_no = make_string(sheet['A' + s_row].value)
            Comic.publisher = sheet['C' + s_row].value
            Comic.sort_name = sheet['D' + s_row].value
            Comic.name = str(sheet['E' + s_row].value)
            t_year = sheet['F' + s_row].value
            if t_year == None:
                Comic.year = 0
            else:
                Comic.year = int(t_year)
            Comic.vol_no = make_string(sheet['G' + s_row].value)
            Comic.issue = make_string(sheet['H' + s_row].value)
            Comic.issue_text = make_string(sheet['I' + s_row].value)
            Comic.grade = make_string(sheet['K' + s_row].value)
            Comic.price = Decimal(sheet['L' + s_row].value)
            Comic.quantity = int(sheet['M' + s_row].value)
            Comic.si = make_string(sheet['N' + s_row].value)
            Comic.issue_notes = make_string(sheet['J' + s_row].value)
            if Comic.issue_notes > '':
                Comic.issue_notes += ' '
            Comic.issue_notes += make_string(sheet['O' + s_row].value)
            Comic.grade_notes = make_string(sheet['P' + s_row].value)
            Comic.inserts = make_string(sheet['Q' + s_row].value)

            try:
                c_issue = Issue.objects.get(catalog_id=Comic.catalog_no)

                # Check items with variants to see if only newsstand is variant
                if c_issue.variants is not None and len(c_issue.variants) > 1:  # corrected variants hold "V"
                    issues = GcdIssue.objects.filter(series_id=c_issue.gcd_series_id, number=c_issue.number,
                                                     variant_of_id__isnull=True)
                    if len(issues) == 1:
                        c_issue.variants = "V"
                        c_issue.gcd_id = issues[0].id
                        scrape_image(c_issue.gcd_id)
                        c_issue.save()
                        print('fixing', Comic.catalog_no)
                        # if issues[0].variant_name.find('Newsstand') != -1:
                        #     # Use issue 1
                        #     c_issue.variants = "V"
                        #     c_issue.gcd_id = issues[1].id
                        #     scrape_image(c_issue.gcd_id)
                        #     c_issue.save()
                        #     print('fixing', Comic.catalog_no)
                        # elif issues[1].variant_name.find('Newsstand') != -1:
                        #     # use issue 2
                        #     c_issue.variants = "V"
                        #     c_issue.gcd_id = issues[0].id
                        #     scrape_image(c_issue.gcd_id)
                        #     print('fixing', Comic.catalog_no)
                        #     c_issue.save()
                        # else:
                        #     messages.append((Comic.catalog_no, Comic.name, Comic.vol_no, Comic.issue, Comic.year,
                        #                     "Variants: " + c_issue.variants))
                    else:
                        messages.append((Comic.catalog_no, Comic.name, Comic.vol_no, Comic.issue, Comic.year,
                                        "Variants: " + c_issue.variants))

                continue

            except ObjectDoesNotExist:
                messages.append((Comic.catalog_no, Comic.name, Comic.vol_no, Comic.issue, Comic.year,
                                 "Not on database"))
                continue  # Temp for fixing variants

        context = {'errors': messages,
                   }
        return render(
            request, self.template_name, context
        )



