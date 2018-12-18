from bs4 import BeautifulSoup

class FilmwebScrappingStrategy:
    def __init__(self, pages_from=None, pages_to=None):
        self.pages_from = pages_from
        self.pages_to = pages_to
        self.mainUrl = 'http://www.filmweb.pl/articles?page={}'

    def parse_page(self, page, download_page_fun):
        soup = BeautifulSoup(page, 'html.parser')

        [x.extract() for x in soup.findAll('script')]   # remove  javascript code
        article_content_div = soup.find('div', attrs={'class': 'articleContent'})

        if(article_content_div == None):
            article_content_div = soup.find('div', attrs={'class': 'newsContent'})

        article_title_div = soup.find('h1', attrs={'itemprop': 'headline'})  # find article title

        if(article_title_div == None):
            article_title_div = soup.find('h1', attrs={'class': 'inline'})  # find article title

        article = article_title_div.text.strip() + "\n" \
                  + article_content_div.text.strip() # strip() is used to remove starting and trailing

        return article

    def parse_urls(self, page):
        soup = BeautifulSoup(page, 'html.parser')


        urls = soup.find('ul', attrs={'class': 'sep-hr'})\
                .find_all('a', attrs={'class': 'hdr'})

        urls = [url['href'] for url in urls]
        urls = ['http://www.filmweb.pl'+url+'\n' for url in urls]
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
                if (new_urls.__len__() == 0):
                    break;
            except Exception as e:
                print('exception{}'.format(e))
                page = download_page_fun(self.mainUrl.format(i))
                new_urls = self.parse_urls(page)

            print('page {}'.format(i))
            urls += new_urls
            urls_file.write(''.join(new_urls).encode('utf-8'))

        urls_file.close()