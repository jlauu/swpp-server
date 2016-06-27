import requests, string, json
from stop_words import get_stop_words
from bs4 import BeautifulSoup as BS

stop_words = get_stop_words('english')

def main(*urls):
    kws = {}
    fix = lambda url: url if 'http://' in url else 'http://'+url
    for url in [u for u in map(fix, urls)]:
        kws[url] = keywords(url)
    return json.dumps(kws, indent=4, separators=(',',': '))

def keywords(url):
    ua = 'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    try:
        r = requests.get(url, headers={'User-Agent': ua})
    except requests.exceptions.ConnectionError:
        return []
    if r.status_code != 200:
        raise IOError
    parser = BS(r.text, 'lxml')
    kws = []
    if parser.title.string:
        kws.extend(parser.title.string.split(' '))
    for meta in [ x['content']for x in
            parser.find_all(attrs={'name':'description'})]:
        kws.extend(meta.split())
    text = ''.join([c for c in ' '.join(kws) if c in
        string.ascii_letters+'\'- ']).lower()
    return list(set(w for w in text.split(' ') if w and w not in stop_words and w not in string.punctuation))
 
if __name__ == '__main__':
    import sys
    print(main(*sys.argv[1:]))
