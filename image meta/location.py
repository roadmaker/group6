#Usage
# from .location import Location
#Location.location(x.photo)
from PIL.ExifTags import GPSTAGS

from PIL import Image

from PIL.ExifTags import TAGS

import re
import base64
from io import BytesIO
 
 
 
def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img

def get_exif(filename):
    try:
        image = base64_to_image(filename)
        # print(filename)
        
        # image = Image.open(filename)
        # image=filename.decode('base64')
        image.verify()

    except Exception as e: print(e)

    print("hiii")
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging
def get_decimal_from_dms(dms, ref):
    try:
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0
    except TypeError:
        degrees = dms[0] 
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def location(file):
    try:

        exif = get_exif(file)
        
        # print(get_geotagging(exif))
        geotags = get_geotagging(exif)
        
        return get_coordinates(geotags)
    except:
        return('not found','not found')
