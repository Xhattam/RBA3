from __future__ import annotations
import streamlit as st
from typing import List, Dict

from pathlib import Path
from datetime import datetime

from PIL import Image, ExifTags

from models.image_metadata import RecordMetadata

import pandas as pd


def extract_with_pillow(image_path: str | Path) -> Dict:
    path = Path(image_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")

    base_meta = {
        "date": None,
        "creator": "",
        "file_name": path.stem,
        "folder_name": str(path.parent),
        "type": "photograph",
        "format": (path.suffix.lstrip(".").lower() or None),
        "language": "english",
    }

    with Image.open(path) as img:
        raw_exif = img.getexif() or {}

    exif = {ExifTags.TAGS.get(tag_id, tag_id): value for tag_id, value in raw_exif.items()}

    date_value = (
        exif.get("DateTimeOriginal")
        or exif.get("DateTimeDigitized")
        or exif.get("DateTime")
    )
    if isinstance(date_value, bytes):
        date_value = date_value.decode(errors="replace")

    base_meta["date"] = str(date_value).strip() if date_value else datetime.now().isoformat(timespec="seconds")

    creator_value = exif.get("Artist") or exif.get("Creator")
    if isinstance(creator_value, bytes):
        creator_value = creator_value.decode(errors="replace")
    base_meta["creator"] = str(creator_value).strip() if creator_value else ""

    try:
        RecordMetadata(**base_meta)
        return base_meta
    except Exception as e:
        print(f"Error creating RecordMetadata: {e}")
        return {"file_name": path.stem, "folder_name": str(path.parent), "error": str(e)}



def get_image_files(folder_path: Path) -> List[str]:
    """Get all image files in a folder."""
    image_files = []
    for file_path in folder_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            image_files.append(str(file_path))
    return image_files


df = pd.DataFrame()
metadata_list = []

st.title("Select a Folder")

folder_input = st.text_input(
    "Enter the folder path",
    placeholder=r"C:\Users\YourName\Documents",
)

if st.button("Select Folder"):
    if not folder_input.strip():
        st.warning("Please enter a folder path.")
    else:
        folder_path = Path(folder_input).expanduser().resolve()

        if folder_path.is_dir():
            st.success("Folder selected")
            st.write("Absolute folder path:")
            st.code(str(folder_path))
            image_files = get_image_files(folder_path)
            st.code(f"Found {len(image_files)} images!")
            st.code("Extracting image metadata...")
            for image_file in image_files:
                img_meta = extract_with_pillow(image_file)
                metadata_list.append(img_meta)
                st.write(f"Image: {image_file}")
                #st.write(f"Metadata: {img_meta.model_dump_json(indent=2)}")

            df = pd.DataFrame(metadata_list)
            st.code("Creating CSV file...")
            df.to_excel(Path(folder_path / "metadata.xlsx"), index=False)

            # Also prints to the terminal running Streamlit
            print(f"Absolute folder path: {folder_path}")
        else:
            st.error("The folder does not exist or is not a directory.")