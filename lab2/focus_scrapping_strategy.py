from bs4 import BeautifulSoup

class FocusScrappingStrategy:
    def __init__(self, pages_from=None, pages_to=None):
        self.pages_from = pages_from
        self.pages_to = pages_to
        self.mainUrl = 'http://www.focus.pl/artykuly?page={}'

    def parse_page(self, page):
        try:
            soup = BeautifulSoup(page, 'html.parser')
        except Exception as e:
            print('exception: {}'.format(e))
            return self.parse_page(page)

        [x.extract() for x in soup.findAll('script')]   # remove  javascript code
        [x.extract() for x in soup.findAll('div', attrs={'id': 'burda-injected-video-row'})]
        article_content_div = soup.find('div', attrs={'class': 'article-body'})    # find article content
        article_title_div = soup.find('h1', attrs={'itemprop': 'name'})      # find article title
        article = article_title_div.text.strip() + "\n" \
                  + article_content_div.text.strip()  # strip() is used to remove starting and trailing
        return article

    def parse_urls(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        urls = soup.find('div', attrs={'class': 'box-article-list'})\
            .find_all('div', attrs={'class': 'box-link-item'})\

        urls = [url.find('a')['href'] for url in urls]
        urls = ['http://focus.pl'+url+'\n' for url in urls]
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