from bs4 import BeautifulSoup as bs
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from urllib.request import Request
import os
import sys

def main(url, out_folder="C:/Users/Pawel1/Desktop/PJN/lab1/test"):
    page = download_page(url)
    parse_text(page, out_folder)
    parse_images(url, page, out_folder)


def _usage():
    print("usage: python main.py http://example.com [outpath]")

# download page from specified url
def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
       'Connection': 'keep-alive'}
    request = Request(url=url, headers=headers)
    try:
        page = urlopen(request, timeout=3)
        return page
    except Exception as e:
        print('exception download_page: {}'.format(e))

# Parse text from url and save it to file text.txt
def parse_text(page, out_folder):
    soup = bs(page, "html.parser")
    [x.extract() for x in soup.findAll('script')]
    page_html = soup.find('body')
    text = page_html.text.strip().encode('utf-8')
    print(text)
    outpath = os.path.join(out_folder, "text.txt")
    save_file = open(outpath, "wb")
    save_file.write(text)
    save_file.close()

# Parse images from url and save them to files in
def parse_images(url, page, out_folder):
    soup = bs(page, "html.parser")
    [x.extract() for x in soup.findAll('script')]
    parsed = list(urlparse(url))

    for image in soup.findAll("img"):
        print("Image: %(src)s" % image)
        filename = image["src"].split("/")[-1]
        parsed[2] = image["src"]
        outpath = os.path.join(out_folder, "images", filename)
        if image["src"].lower().startswith("http"):
            urlretrieve(image["src"], outpath)
        else:
            urlretrieve(urlunparse(parsed), outpath)

if __name__ == "__main__":
    sys_arg_len = len(sys.argv)
    out_folder = "./"

    if(sys_arg_len <= 1):
        _usage()
        sys.exit(-1)

    if(sys_arg_len > 1):
        url = sys.argv[1]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)

    if(sys_arg_len > 2):
        out_folder = sys.argv[2]

    main(url, out_folder)

