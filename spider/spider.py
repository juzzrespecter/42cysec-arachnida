#!/usr/bin/python3

from urllib.request import Request
import requests, sys, argparse, os, time, threading
from bs4 import BeautifulSoup
from os.path import exists, isdir, basename, splitext
from urllib.parse import urlparse

allowed_ext = ['.jpg','.jpeg','.png','.gif','.bmp']
allowed_scheme = ['http']

url_log = set()
url_log_lock = threading.Lock()

def parse_args() -> str:
    parser = argparse.ArgumentParser(prog='spider.py', description='** Get-IP-banned utility **')
    parser.add_argument('-r', help='recursive scrapping in URL', action='store_true')
    parser.add_argument('-l', help='set up recursion level (needs -r)', type=int,
                          nargs='?', metavar=('N'), default=1) 
    parser.add_argument('-p', help='indicate path to downloads', type=str,
                        nargs=1, metavar=('PATH'), default=['./data/'])
    parser.add_argument('URL', type=str)
    args = parser.parse_args()

    global recursion_level, download_path
    recursion_level = 0
    if args.r:
        recursion_level = args.l
    if recursion_level < 0:
        print(f'{recursion_level} is an invalid recursion level, exiting...', file=sys.stderr)
        sys.exit(1)
    download_path = args.p[0]
    if download_path[-1] != '/':
        download_path += '/'
    print(download_path)
    url = args.URL
    if url[-1] == '/':
        url = url[:-1]
    return url

def generate_url(url: str, domain: str) -> str:
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        url = domain + url
    elif not url.startswith('http'):
        url = domain + '/' + url
    return url

def img_name_generator(img_url: str) -> str:
    img_path = urlparse(img_url).path
    img_name = basename(img_path)
    name_s = splitext(img_name)
    for ext in allowed_ext:
        if ext == name_s[1]:
            new_name = name_s[0]
            i = 1
            while exists(download_path + new_name + name_s[1]) and i < 1000:
                new_name = name_s[0] + '_' + str(i)
                i += 1
            if i == 1000:
                raise Exception('too many files with name ' + img_name)
            return download_path + new_name + name_s[1]
    raise Exception('Not valid ext.: ' + name_s[1])

def request_img(img: str, root: str):
    try:
        img_url = img['src']
        if not img_url:
            sys.exit(0)
        img_url = generate_url(img_url, root)
        with url_log_lock:
            if img_url in url_log:
                sys.exit(0)
            url_log.add(img_url)
        img_req = requests.get(img_url, verify=True, timeout=5)
        if img_req.status_code != 200:
            sys.exit(0)
        img_name = img_name_generator(img_url)
        with open(img_name, 'wb+') as f:
            f.write(img_req.content)
    except MemoryError:
        print('No space left on device', sys.stderr)
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

def scrap_request(req: Request, root: str):
    imgs = BeautifulSoup(req.text, 'lxml').find_all('img')
    img_threads = []
    for img in imgs:
        thr = threading.Thread(target=request_img, args=[img, root])
        thr.start()
        img_threads.append(thr)
    for thread in img_threads:
        thread.join()
        
def petition_layer(url: str, l: int):
    l += 1
    print(f'Scrapping url {url} [ RL {str(l)} ]')
    p = urlparse(url)
    root = p.scheme + "://" + p.hostname
    try:
        url_log.add(url)
        req = requests.get(url, verify=True, timeout=5)
    except Exception:
        print(f'[!!] Failed to request page {url}', file=sys.stderr)
        return
    scrap_request(req, root)
    if l >= recursion_level:
        return
    links = BeautifulSoup(req.text, 'lxml').find_all('a')
    for link in links:
        try:
            href = link['href']
        except:
            continue
        if not href:
            continue
        if href[-1] == '/':
            href = href[:-1]
        href = generate_url(href, root)
        if href in url_log or (urlparse(href).scheme not in ['http','https']):
            continue
        petition_layer(href, l)

def main() -> int:
    url = parse_args()
    if urlparse(url).scheme not in ['http','https']:
        print(f'[{url}]: wrong url provided')
        return 1
    if not exists(download_path) or not isdir(download_path):
        try:
            os.mkdir(download_path)
        except:
            print('Could not create dest. directory', sys.stderr)
            return 1
    t_start = time.perf_counter()
    petition_layer(url, -1) # asdasd
    t_end = time.perf_counter()
    print(f'Scraping took {t_end - t_start} s')

if __name__ == "__main__":
    sys.exit(main())
