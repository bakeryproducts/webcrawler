import random
import string
from urllib.parse import urlparse
from multiprocessing import Pool

import bs4 as bs
import requests
from urllib.parse import urljoin


def get_links(url):
    try:
        print('trying ',url)
        resp = requests.get(url,timeout=3)

        soup = bs.BeautifulSoup(resp.text, 'lxml')
        body = soup.body
        links = [urljoin(url, link.get('href')) for link in body.find_all('a') if is_good(link.get('href'))]
        links.append(url)
        return list(set(links))

    except requests.ReadTimeout:
        print('cant get response!')
        return [url]
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
    st = ''.join(['http://', st, '.com'])
    return st


def get_dom(url):
    try:
        dom = urlparse(url).hostname
        dom = ''.join(['http://',dom])
    except:
        return ''
    return dom

def main():
    visited_domains = []
    visited_urls = []
    cnt = 3
    p = Pool(processes=10)
    to_parse = [url_gen() for _ in range(cnt)]

    fd = open('domains.txt','w')
    fu = open('urls.txt','w')
    i=0
    while i<20 and len(to_parse)>0 and 'youtube' not in visited_domains:
        data = p.map(get_links, to_parse)
        links = [url for site in data for url in site]
        print(links)

        to_parse = list(set([get_dom(url) for url in links if get_dom(url) not in visited_domains]))
        visited_urls.extend(links)
        visited_urls = list(set(visited_urls))
        visited_domains.extend([get_dom(link) for link in links])
        visited_domains = list(set(visited_domains))
        i+=1
        fd.write('\n'.join(visited_domains))
        fu.write('\n'.join(visited_urls))
        print('-------------------------------------end-iteration------------------------------------------------')

    p.close()
    fd.close()
    fu.close()

    print('THE END: visited {} urls in {} domains. worked for {} iterations'.format(len(visited_domains),len(visited_urls),i))

if __name__ == '__main__':
    main()
