# from fastapi import Depends, HTTPException, status, FastAPI, Request
# from fastapi.exceptions import RequestValidationError
#

#
# app = FastAPI(name="RBA3 - Reading Berkshire Archives Automation App")
#
# @app.get("/health")
# def health_check():
#     return {"status": "ok"}
#

#from config import settings
#from utils.llm_utils import qwen_llm

#from core.extract_metadata import QwenImageToText

#qwen_class = QwenImageToText()

img_path = "data/sample_pictures/014.JPG"

# res = qwen_class.describe_image(img_path)
# Source - https://stackoverflow.com/a/21698063
# Posted by Mzzl, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-29, License - CC BY-SA 4.0

from PIL import Image, ExifTags
import datetime
import os

def extract_with_pillow(img_path: str) -> dict:
    meta = {
        k: '' for k in
        ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized', 'Copyright', 'Artist']
    }
    meta = {
        'date': None,
        'creator': None,
        'file_name': None,
        'folder_name': None,
        'type': None,
        'format': None,
        'language': None
    }
    img = Image.open(img_path)
    for k, v in img._getexif().items():

        if k == 'DateTimeOriginal' and not meta['date']:
            meta['date'] = v
        elif k

    meta['date'] = exif.get(
        'DateTimeOriginal', exif.get(
            'Datetime', exif.get(
                'DateTimeOriginal', datetime.now()
            )
        )
    )
    meta['creator'] = exif.get('Artist', exif.get('Creator', ''))

    # TODO add try/except in case
    folder_name, file_info = img_path.rsplit(os.sep, 1)
    file_name, format = file_info.rsplit('.', 1)

    meta['folder_name'] = folder_name
    meta['file_name'] = file_name
    meta['format'] = format
    meta['type'] = 'photograph'
    meta['language'] = 'english'

    exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
    return {k: v.strip() for k, v in exif.items() if k in meta and v.strip() != ''}



res = extract_with_pillow(img_path)
print(res)

#img = Image.open(img_path)
#exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }

#print(ExifTags.TAGS)
#
# for k, v in exif.items():
#     if k != "MakerNote":
#         print(f"{k}: {v}")

# print(res)
