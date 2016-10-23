from django.shortcuts import render
from django.views.generic.list import  View
from django.core.exceptions import ObjectDoesNotExist
import os.path
from comix.models import  Issue
from django.conf import settings as djangoSettings


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
        if djangoSettings.STATIC_ROOT != None:
            saved_filename =  djangoSettings.STATIC_ROOT + '/bigImages/' + filename
        else: # debug version
            saved_filename = 'comix/static/bigImages/' + filename
        if not os.path.isfile(saved_filename):
            print("Scraping image issue", gcd_issue_id)
            urllib.request.urlretrieve(src_filename, saved_filename)
            sleep(1)
            # Now create thumbnail
            size = (100, 156)
            if djangoSettings.STATIC_ROOT != None:
                thumb_filename = djangoSettings.STATIC_ROOT + '/thumbnails/' + filename
            else:
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
                issue = cat_id


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
            issue.variants = ''
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


# Variant images must be loaded on a test machine, pushed to github, pulled to the production machine, and then
# collectstatic run.
class LoadVariantsView(View):
    template_name = 'imports/variants.html'
    gcd_series_recs = None

    def get(self, request):
        images = []
        error = ''
        # User clicked so select an image,so update it on record and clear variant field
        issues = Issue.objects.filter(variants__isnull=False)
        for issue in issues:
            images = scrape_images(issue.gcd_id)
            debug(images)
            issue.variants += 'scraped,'
            issue.save()
            context = {
                'title': 'Success!',
                'error': '',
                'images': [],
                'cat_id': '',
            }


        return render(
            request, self.template_name, context
        )

