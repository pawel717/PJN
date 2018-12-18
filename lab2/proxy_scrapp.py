from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# Script to gather free proxies from https://www.sslproxies.org/

proxies=[]

proxies_req = Request('https://www.sslproxies.org/')

proxies_doc = urlopen(proxies_req).read().decode('utf8')

soup = BeautifulSoup(proxies_doc, 'html.parser')
proxies_table = soup.find(id='proxylisttable')

for row in proxies_table.tbody.find_all('tr'):
  proxies.append({
    'ip':   row.find_all('td')[0].string,
    'port': row.find_all('td')[1].string
  })

print(proxies)