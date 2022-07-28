#!/usr/bin/python3
import sys, argparse
from exif import Image
from os.path import splitext

allowed_ext = ['.jpg','.jpeg','.png','.gif','.bmp']

def main() -> str:
    parser = argparse.ArgumentParser(prog="scorpion.py", 
                                     description="Metadata analysis for imgs")
    parser.add_argument('FILE', nargs='+', type=str)
    args = parser.parse_args()
    for file in args.FILE:
        file_p = splitext(file)
        if file_p[1] in allowed_ext:
            try:
                with open(file, 'rb') as f:
                    img = Image(f)
                    if img.has_exif:
                        print(f'----------< {file} >----------')
                        try:
                            for tag in dir(img):
                                print(f'[ {tag} ] : {img.get(tag)}')
                        except Exception as e:
                            print(str(e))
                            continue
                    else:
                        print(f'file {file} has no EXIF present')
            except:
                print(f'Could not open file {file} for reading')
                continue

if __name__ == "__main__":
    sys.exit(main())