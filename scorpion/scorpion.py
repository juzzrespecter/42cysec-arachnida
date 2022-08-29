#!/usr/bin/python3
import sys, argparse
from PIL import Image
from exifread import process_file
#from PIL.ExifTags import TAGS
from os.path import splitext

allowed_ext = ['.jpg','.jpeg','.png','.gif','.bmp']
bad_tags = ['JPEGThumbnail', 'EXIF ExifImageWidth', 'EXIF ExifImageLength']

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
        print(f'[ {attr:37} ] : {val}')
    
def not_exif_tag(tag_id):
    return tag_id.startswith('Makernote') or tag_id.startswith('Thumbnail')

def print_exif_tags(file: str):
    try:
        with open(file, "rb+") as f:
            tags = process_file(f)
            if not tags:
                print(f'[!!] no EXIF metadata present in {file}.')
                return
            for tag_id in tags.keys():
                if (tag_id in bad_tags) or not_exif_tag(tag_id):
                    continue
                print(f'[ {tag_id:37} ] : {tags[tag_id]}')
    except Exception as e:
        print(f'[!!] error reading metadata: {str(e)}')
        return 

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
                    print_exif_tags(file)
            except Exception as e:
                print(f'[!!] error reading metadata: {str(e)}')
                continue
        else:
            print(f'[!!] format not allowed in file {file}')

if __name__ == "__main__":
    sys.exit(main())
