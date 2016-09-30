def scrape_image(gcd_issue_id):
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

scrape_image(26679)