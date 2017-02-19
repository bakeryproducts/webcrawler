import random
import string
import time
from urllib.parse import urlparse
from multiprocessing import Pool
from urllib.request import urlopen

import bs4 as bs
import requests
from urllib.parse import urljoin


def get_links(url):
    try:
        start_time = time.time()
        print('trying ',url)
        resp = requests.get(url)
        print('response!')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        body = soup.body
        links = [urljoin(url, link.get('href')) for link in body.find_all('a') if is_good(link.get('href'))]
        links.append(url)
        return list(set(links))
    except Exception as e:
        #print(e)
        return [url]


def is_good(url):
    ban_list = ('mailto:', 'tel:', 'javascript:', 'skype:',
                '.ppt', '.jpg', '.doc', '#', '.png', '.gif', '.rar', '.zip', 'tg:', '*', '.pdf', 'mp4', '.asp','.xls')
    for el in ban_list:
        if el in url:
            return False
    return True


def url_gen():
    st = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(3))
    st = ''.join(['http://', st, '.ru'])
    return st


def get_dom(url):
    dom = urlparse(url).hostname
    dom = ''.join(['http://',dom])
    return dom

def main():
    visited_domains = []
    visited_urls = []
    cnt = 5
    p = Pool(processes=10)
    #to_parse = [url_gen() for _ in range(cnt)]
    to_parse = ['http://ed.gov.ru']
    i=0
    while i<10 and len(to_parse)>0 and 'http://www.youtube.com' not in visited_domains:
        data = p.map(get_links, to_parse)
        links = [url for site in data for url in site]
        print(links)

        to_parse = list(set([get_dom(url) for url in links if get_dom(url) not in visited_domains]))
        print('and parse: ',to_parse)
        visited_urls.extend(links)
        visited_urls = list(set(visited_urls))
        visited_domains.extend([get_dom(link) for link in links])
        visited_domains = list(set(visited_domains))
        i+=1

    with open('domains.txt', 'w') as fd:
        fd.write('\n'.join(visited_domains))
    with open('urls.txt', 'w') as fu:
        fu.write('\n'.join(visited_urls))
    p.close()
    print(len(visited_domains),' ',len(visited_urls))
if __name__ == '__main__':
    main()
