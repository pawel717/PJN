# import libraries
import json
import mysql.connector
import sys
import scrapper
from proxy_provider import ProxyProvider
from newonce_scrapping_strategy import  NewonceScrappingStrategy
from focus_scrapping_strategy import  FocusScrappingStrategy
from ngeographic_scrapping_strategy import NationalGeographicScrappingStrategy
from filmweb_scrapping_strategy import FilmwebScrappingStrategy

def _usage():
    print("usage: python main.py mode site")
    print("mode - gatherUrls, scrape")
    print("site - newonce, focus, national-geographic, filmweb")
    sys.exit(-1)

config = json.load(open('config.json'))

mydb = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    passwd=config['mysql']['passwd'],
    database=config['mysql']['database'],
    use_unicode=config['mysql']['use_unicode']
)

cursor = mydb.cursor()

# Enforce UTF-8 for the connection.
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

# Commit data.
mydb.commit()

proxyProvider = ProxyProvider()
proxyProvider.proxies = config['proxies']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
       'Connection': 'keep-alive'}

myScrapper = scrapper.Scrapper()
myScrapper.proxyProvider = proxyProvider
myScrapper.headers = headers
myScrapper.saveFile = open("./text.txt", "ab")
myScrapper.myDb = mydb

if(len(sys.argv) < 3):
    _usage()

mode = sys.argv[1]
site = sys.argv[2]

# Set proper scrapping strategy based on program argument 'site'
if(site == 'newonce'):
    scrappingStrategy = NewonceScrappingStrategy()
    scrappingStrategy.pages_from = 0
    scrappingStrategy.pages_to = 1000
elif(site == 'filmweb'):
    scrappingStrategy = FilmwebScrappingStrategy()
    scrappingStrategy.pages_from = 0
    scrappingStrategy.pages_to = 1000
elif(site == 'focus'):
    scrappingStrategy = FocusScrappingStrategy()
    scrappingStrategy.pages_from = 0
    scrappingStrategy.pages_to = 1000
elif(site == 'national-geographic'):
    scrappingStrategy = NationalGeographicScrappingStrategy()
    scrappingStrategy.pages_from = 0
    scrappingStrategy.pages_to = 1000
else:
    _usage()

myScrapper.scrapeStrategy = scrappingStrategy

# Run in proper mode based on program argument 'mode'
if(mode == 'gatherUrls'):
    myScrapper.gather_urls()
elif (mode == 'scrape'):
    urls_file = open(config['urls'], "r+")
    urls = urls_file.read()
    urls = urls.split('\n')
    myScrapper.urls = urls
    myScrapper.start_scraping()
else:
    _usage()