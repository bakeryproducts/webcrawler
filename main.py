import random
import string
from urllib.parse import urlparse
from multiprocessing import Pool
import sys
import bs4 as bs
import requests
from urllib.parse import urljoin


def get_links(url):
    try:
        print('In ', url, end='\tcollected ')
        resp = requests.get(url, timeout=3)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        body = soup.body
        links = [urljoin(url, link.get('href')) for link in body.find_all('a') if is_good(link.get('href'))]
        links.append(url)
        print('{} new urls'.format(len(links)))
        return list(set(links))

    except requests.ReadTimeout:
        print('cant get response!')
        return []
    except TypeError:
        #return [url[:4]+'s'+url[4:]]
        return []
    except Exception as e:
        print(e,'only errors...', )  # catched  e
        #print("Unexpected error:", sys.exc_info()[0])
        return []


def is_good(url):
    ban_list = ('mailto:', 'tel:', 'javascript:', 'skype:',
                '.ppt', '.jpg', '.doc', '#', '.png', '.gif', '.rar', '.zip', 'tg:', '*', '.pdf', 'mp4', '.asp', '.xls')
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
        dom = ''.join(['http://', dom])
    except Exception as e:
        return ''
    return dom


def main():
    visited_domains = []
    visited_urls = []
    cnt = 3
    p = Pool(processes=10)
    # to_parse = [url_gen() for _ in range(cnt)]
    to_parse = ['https://telegram.org']
    i = 0
    while i < 20 and len(to_parse) > 0 and 'youtube' not in visited_domains:
        data = p.map(get_links, to_parse)
        links = [url for site in data for url in site]

        if i<3:
            to_parse = list(set([url for url in links]))
        else:
            to_parse = list(set([get_dom(url) for url in links if get_dom(url) not in visited_domains]))

        visited_urls.extend(links)
        visited_urls = list(set(visited_urls))
        visited_domains.extend([get_dom(link) for link in links])
        visited_domains = list(set(visited_domains))
        i += 1
        with open('domains.txt', 'w') as fd:
            fd.write('\n'.join(visited_domains))
        with open('urls.txt', 'w') as fu:
            fu.write('\n'.join(visited_urls))
        print(to_parse)
        print('--------------------------end--of--iteration--{}-------------------------------------'.format(i))

        for dom in visited_domains:
            if 'wikipedia' in dom:
                break
        else:
            continue
        break

    p.close()

    print('THE END: visited {} urls in {} domains. worked for {} iterations'.format(len(visited_urls),
                                                                                    len(visited_domains), i))


if __name__ == '__main__':
    main()
