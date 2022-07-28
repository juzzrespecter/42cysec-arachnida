#!/usr/bin/python3

import requests, sys, argparse, os, asyncio, time
from bs4 import BeautifulSoup
from os.path import exists, isdir, basename, splitext
from urllib.parse import urlparse

allowed_ext = ['.jpg','.jpeg','.png','.gif','.bmp']
allowed_scheme = ['http']
url_log = set()

def parse_args() -> str:
    parser = argparse.ArgumentParser(prog='42cysec-arachnida', description='** get-IP-banned utility **')
    parser.add_argument('-r', help='recursive scrapping in URL', action='store_true')
    parser.add_argument('-l', help='set up recursion level (needs -r)', type=int,
                          nargs='?', metavar=('N'), default=1) 
    parser.add_argument('-p', help='indicate path to downloads', type=str,
                        nargs=1, metavar=('PATH'), default='./data/')
    parser.add_argument('URL', type=str)
    args = parser.parse_args()

    global recursion_level, download_path
    recursion_level = 1
    if args.r:
        recursion_level = args.l
    download_path = args.p
    return args.URL

def img_name_generator(img_url: str) -> str:
    name = basename(img_url)
    name_s = splitext(name)
    for ext in allowed_ext:
        if ext == name_s[1]:
            new_name = name_s[0]
            i = 1
            while exists(download_path + new_name + name_s[1]) and i < 1000:
                new_name = name_s[0] + '_' + str(i)
                i += 1
            if i == 1000:
                raise Exception('too many files with name ' + name)
            return download_path + new_name + name_s[1]
    raise Exception('Not valid ext.: ' + name_s[1])

def petition_layer(url: str, l: int):
    l += 1
    print('l: ' + str(l))
    print('url: ' + url)
    p = urlparse(url)
    root = p.scheme + "://" + p.hostname
    print('root: ' + root)
    try:
        url_log.add(url)
        req = requests.get(url)
    except Exception:
        print('[LOG] Failed to request page ' + url, file=sys.stderr)
        return

    imgs = BeautifulSoup(req.text, 'lxml').find_all('img')
    for img in imgs:
        try:
            img_url = img['src']
        except:
            continue
        try:
            if not img_url:
                continue
            if img_url[0] == '/':
                img_url = root + img_url
            if img_url in url_log:
                continue
            url_log.add(img_url)                
            img_req = requests.get(img_url)
            if img_req.status_code != 200:
                continue
            img_name = img_name_generator(img_url)
            with open(img_name, 'wb+') as f:
                f.write(img_req.content)
        except Exception as e:
            print('[LOG] Failed to request img: ' + str(e))
            continue
    if l >= recursion_level:
        return
    links = BeautifulSoup(req.text, 'lxml').find_all('a')
    for link in links:
        href = link['href']
        print('href: ' + href)
        if not href:
            continue
        sch = urlparse(href).scheme
        if not sch:
            href = root + href
        if href[-1] != '/':
            href += '/'
        if href in url_log or (sch not in ['http','https']):
            continue
        petition_layer(href, l)

def main() -> int:
    url = parse_args()
    if not exists(download_path) or not isdir(download_path):
        try:
            os.mkdir(download_path)
        except:
            print('Could not create dest. directory', sys.stderr)
            return 1
    petition_layer(url, 0)

if __name__ == "__main__":
    sys.exit(main())
