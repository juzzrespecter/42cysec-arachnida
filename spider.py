#!/usr/bin/python3

import requests, sys, argparse
from bs4 import BeautifulSoup

# -rlpS
# -r es url
# -r -l [N] recursiva, nivel (sin -l por defecto es 5)
# -p path a guardar, no indicarse es ./data

allowed_files = ['.jpg','.jpeg','.gif','.bmp']
recursion_level = 1
download_path = './data/'

# request
# beautify
# get images
# search for links
# call

# image:
# find image url
# petition to img url
# get img name
# open & write

def petition_manage_req(req):
    soup = BeautifulSoup(req.text, features="html.parser").a

    for a in soup.find_all('a'):
        print(a.length)
    for button in soup.find_all('button'):
        print('hola')
    print('hola')
    
    

def petition_layer(url: str, l: int):
    try:
        req = requests.get(url)
    except Exception as e:
        print('oh no!' + e)
    else:
        petition_manage_req(req)
    

def main() -> int:
    parser = argparse.ArgumentParser(prog='42cysec-arachnida', description='** get-IP-banned utility **')
    parser.add_argument('-r', help='recursive scrapping in URL', action='store_true')
    parser.add_argument('-l', help='set up recursion level (needs -r)', type=int,
                          nargs='?', metavar=('N'), default=1) 
    parser.add_argument('-p', help='indicate path to downloads', type=str,
                        nargs=1, metavar=('PATH'), default='./data/')
    parser.add_argument('URL', type=str)
    args = parser.parse_args()

    global recursion_level
    global download_path
    recursion_level = args.l
    download_path = args.p
    petition_layer(args.URL, 1)
    

if __name__ == "__main__":
    sys.exit(main())
