from bs4 import BeautifulSoup

class NationalGeographicScrappingStrategy:
    def __init__(self, pages_from=None, pages_to=None):
        self.pages_from = pages_from
        self.pages_to = pages_to
        self.mainUrl = 'http://www.national-geographic.pl/national-geographic/?page={}'

    def parse_single_page(self, page, download_page_fun):
        soup = BeautifulSoup(page, 'html.parser')

        [x.extract() for x in soup.findAll('script')]  # remove  javascript code
        article_content_div = soup.find('div', attrs={'class': 'article-body'})  # find article content

        return article_content_div.text.strip()  # strip() is used to remove starting and trailing


    def parse_page(self, page, download_page_fun):
        soup = BeautifulSoup(page, 'html.parser')

        [x.extract() for x in soup.findAll('script')]   # remove  javascript code
        article_content_div = soup.find('div', attrs={'class': 'article-body'})
        article_title_div = soup.find('h2', attrs={'itemprop': 'name'})  # find article title

        article = article_title_div.text.strip() + "\n" \
                  + article_content_div.text.strip() # strip() is used to remove starting and trailing

        pages = soup.find('div', attrs={'id': 'paging'})
        if(pages):
            pages_urls = pages.find_all('a')
            pages_urls = [page['href'] for page in pages_urls]
            pages_urls = [page.url + single_page.replace('#article-content', '') for single_page in pages_urls]
            for i in range(1, len(pages_urls)):
                single_page = download_page_fun(pages_urls[i])
                article += self.parse_single_page(single_page, download_page_fun)

        return article

    def parse_urls(self, page):
        try:
            soup = BeautifulSoup(page, 'html.parser')
        except Exception as e:
            print('exception parse_urls: {}'.format(e))
            return self.parse_urls(page)

        urls = soup.find('div', attrs={'class': 'ias-list'})\
                .find_all('h2')

        urls = [url.find('a')['href'] for url in urls]
        urls = ['http://www.national-geographic.pl'+url+'\n' for url in urls]
        print("founded urls:")

        print(urls)
        return urls

    def gather_urls(self, download_page_fun):
        if (self.pages_from == None or self.pages_to == None):
            return

        urls_file = open("./urls.txt", "ab")
        urls = []

        for i in range(self.pages_from, self.pages_to):
            page = download_page_fun(self.mainUrl.format(i))
            try:
                new_urls = self.parse_urls(page)
                if(new_urls.__len__() == 0):
                    break;
            except Exception as e:
                print('exception{}'.format(e))
                page = download_page_fun(self.mainUrl.format(i))
                new_urls = self.parse_urls(page)
            print('page {}'.format(i))
            urls += new_urls
            urls_file.write(''.join(new_urls).encode('utf-8'))

        urls_file.close()