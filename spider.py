#!/usr/bin/python3

import http, sys, argparse

# -rlpS
# -r es url
# -r -l [N] recursiva, nivel (sin -l por defecto es 5)
# -p path a guardar, no indicarse es ./data

def main() -> int:
    parser = argparse.ArgumentParser(prog='42cysec-arachnida', description='** get-IP-banned utility **')
    parser.add_argument('-r', help='recursive scrapping in URL', action='store_true')
    parser.add_argument('-l', help='set up recursion level', type=int,
                          nargs='?', metavar=('N'), default=5) 
    parser.add_argument('-p', help='indicate path to downloads', type=str,
                        nargs=1, metavar=('PATH'), default='./data/')
    parser.add_argument('URL', type=str)
    args = parser.parse_args()

if __name__ == "__main__":
    sys.exit(main())
