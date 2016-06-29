import requests, string, json
from stop_words import get_stop_words
from bs4 import BeautifulSoup as BS
from requests.exceptions import *

stop_words = get_stop_words('english')
ua = 'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.103 Safari/537.36'
# Adapted from http://code.lancepollard.com/complete-list-of-html-meta-tags/
common_meta_tags = [
        'keywords',
        'description',
        'subject',
        'abstract',
        'topic',
        'summary',
        'author',
        'designer',
        'owner',
        'identifier-URL',
        'category',
        'coverage',
        'subtitle',
        'medium',
        'syndication-source',
        'original-source',
        'application-name',
        'msapplication-tooltip',
        'tweetmeme-title',
]

def main(*urls):
    kws = {}
    fix = lambda url: url if 'http://' in url or 'https://' in url else 'http://'+url
    for url in urls:
        kws[url] = keywords(fix(url))
    return json.dumps(kws, indent=4, separators=(',',': '))

def keywords(url):
    try:
        r = requests.get(url, headers={'User-Agent': ua})
    except (ConnectionError, InvalidURL) as e:
        print('Cannot connect to:', url)
        raise ConnectionError
    if r.status_code != 200:
        print('Cannot connect to:', url, '(status code:{})'.format(r.status_code))
        raise ConnectionError
    parser = BS(r.text, 'lxml')
    kws = []
    if parser.title and parser.title.string:
        kws.extend(parser.title.string.split(' '))
    for meta in parser.find_all('meta'):
        if 'content' in meta.attrs and 'name' in meta.attrs and meta['name'] in common_meta_tags:
           kws.extend(meta['content'].split())
    text = ''.join([c for c in ' '.join(kws) if c in
        string.ascii_letters+'\'- ']).lower()
    return list(set(w for w in text.split(' ') if w and w not in stop_words and w not in string.punctuation))
 
if __name__ == '__main__':
    import sys
    print(main(*sys.argv[1:]))
