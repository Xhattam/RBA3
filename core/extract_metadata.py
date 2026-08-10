from typing import List, Dict

from pathlib import Path
from datetime import datetime

from PIL import Image, ExifTags

from models.image_metadata import RecordMetadata


def get_size(img_path: Path) -> str:
    """ Get image size in MB """
    try:
        size_bytes = path.stat().st_size
        size_mb = size_bytes / (1024 ** 2)
        return f"{size_mb} MB"
    except:
        return ""

def get_format(img_path: Path) -> str:
    """ Get file extension """
    try:
        return img_path.suffix.lower()
    except:
        return ""

def extract_with_pillow(image_path: str | Path) -> Dict:
    """ Extract image metadata using Pillow """
    path = Path(image_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")

    # base metadata
    base_meta = {
        "file_name": path.stem,
        "folder_name": str(path.parent),
        "format": get_format(path),
        "size": get_size(path)
    }

    with Image.open(path) as img:
        raw_exif = img.getexif() or {}

    exif = {ExifTags.TAGS.get(tag_id, tag_id): value for tag_id, value in raw_exif.items()}

    # date definition, extracted from photo fields when found, otherwise set to today/now
    date_value = (
        exif.get("DateTimeOriginal")
        or exif.get("DateTimeDigitized")
        or exif.get("DateTime")
    )
    if isinstance(date_value, bytes):
        date_value = date_value.decode(errors="replace")

    base_meta["date"] = str(date_value).strip() if date_value else datetime.now().isoformat(timespec="auto")

    # creator field, extracted from photo when available, otherwise set to empty
    creator_value = exif.get("Artist") or exif.get("Creator")
    if isinstance(creator_value, bytes):
        creator_value = creator_value.decode(errors="replace")
    base_meta["creator"] = str(creator_value).strip() if creator_value else ""

    try:
        # validate with pydantic, return as dict ready for final dataframe creation
        record = RecordMetadata(**base_meta)
        return record.model_dump(by_alias=True)
    except Exception as e:
        print(f"Error creating metadata for file {image_path}, please add manually\n{str(e)}")
