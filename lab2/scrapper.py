import time
from urllib.request import urlopen, Request
class Scrapper:

    def __init__(self):
        self.urls = []  # url adresses of sites to scrape
        self.scrapeStrategy = None
        self.delay = 0.1    # delay between requests
        self.proxyProvider = None
        self.headers = {}
        self.saveFile = None
        self.myDb = None
        self.pages_from = None
        self.pages_to = None

    def start_scraping(self):
        for url in self.urls:
            self.scrape(url)

    def scrape(self, url):
        # download page specified by url
        page = self.download_page(url)
        # get text content from page
        try:
            text_content = self.scrapeStrategy.parse_page(page, self.download_page)
        except Exception as e:
            print('exception{}'.format(e))
            return self.scrape(url)
        # save text content to database
        mycursor = self.myDb.cursor()
        insert_query = "INSERT INTO articles (url, text) VALUES (%s, %s)"
        mycursor.execute(insert_query, (url, text_content))
        self.myDb.commit()
        # save text content to file
        self.saveFile.write(text_content.encode('utf-8'))

        print('article from url: {} saved'.format(url))

    def gather_urls(self):
        self.scrapeStrategy.gather_urls(self.download_page)

    def download_page(self, url):
        time.sleep(self.delay)
        request = Request(url=url, headers=self.headers)
        request.set_proxy(self.proxyProvider.getNextProxy(), 'http')
        try:
            page = urlopen(request, timeout=3)
            return page
        except Exception as e:
            print('exception download_page: {}'.format(e))
            return self.download_page(url)

