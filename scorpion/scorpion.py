#!/usr/bin/python3
import sys, argparse
from PIL import Image
from PIL.ExifTags import TAGS
from os.path import splitext

allowed_ext = ['.jpg','.jpeg','.png','.gif','.bmp']

def print_img_attributes(img: Image):
    attr_dic = {
        "name":    img.filename,
        "format":  img.format,
        "mode":    img.mode,
        "size":    img.size,
        "width":   img.width,
        "height":  img.height,
        "is animated": getattr(img, "is_animated", False),
        "frames": getattr(img, "n_frames", 1)
    }
    for attr, val in attr_dic.items():
        print(f'[ {attr:15} ] : {val}')
    

def main() -> str:
    parser = argparse.ArgumentParser(prog="scorpion.py", 
                                     description="Metadata analysis for imgs")
    parser.add_argument('FILE', nargs='+', type=str)
    args = parser.parse_args()
    for file in args.FILE:
        file_p = splitext(file)
        if file_p[1] in allowed_ext:
            try:
                with Image.open(file) as img:
                    print(f'----------< {file} >----------')
                    print_img_attributes(img)
                    try:
                        exif = img.getexif()
                        if not exif:
                            print(f'[!!] file {file} has no EXIF metadata present')
                            continue
                        print(f'----------<  EXIF  >----------')
                        for id in exif:
                            tag = TAGS.get(id, id)
                            data = exif.get(id)
                            if isinstance(data, bytes):
                                data = data.decode()
                            print(f'[ {tag:15} ] : {data}')
                    except Exception as e:
                        print(str(e))
                        continue
            except Exception as e:
                print(f'[!!] error reading metadata for {file}: {str(e)}')
                continue
        else:
            print(f'[!!] format not allowed in file {file}')

if __name__ == "__main__":
    sys.exit(main())
