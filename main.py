from __future__ import annotations
import streamlit as st
from typing import List

from pathlib import Path
from core.extract_metadata import extract_with_pillow

from models.image_metadata import RecordMetadata

import pandas as pd


def get_image_files(folder_path: Path) -> List[str]:
    """Get all image files in a folder."""
    image_files = []
    for file_path in folder_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            image_files.append(str(file_path))
    return image_files


df = pd.DataFrame()
metadata_list = []

st.title("Select a Folder")

folder_input = st.text_input(
    "Enter the full folder path (must only contain flat jpg, jpeg or png files):",
    placeholder=r"C:\Users\YourName\Documents",
)
image_processing_errors = []

if st.button("Select Folder"):
    if not folder_input.strip():
        st.warning("Please enter a folder path.")
    else:
        folder_path = Path(folder_input).expanduser().resolve()

        if folder_path.is_dir():
            st.success("Folder found!")
            st.write(f"Processing folder {folder_path}...")
            image_files = get_image_files(folder_path)
            total_images = len(image_files)
            st.success(f"Found {len(image_files)} images!")
            st.write("Extracting image metadata...")
            for image_file in image_files:
                st.write(f"Processing {image_file}...")
                try:
                    img_meta = extract_with_pillow(image_file)
                    metadata_list.append(img_meta)
                except:
                    st.code(f"Error getting metadata for file {image_file} - skipping")
                    image_processing_errors.append(image_file)

            total_processed = total_images - len(image_processing_errors)

            if image_processing_errors:
                st.warning(f"Processed {total_processed}/{total_images} images")
                st.warning(f"The following files could not be processed: {'\n- '.join(image_processing_errors)}")
            else:
                st.success(f"Done! Processed {total_processed}/{total_images} images")

            columns = [field.alias or field_name for field_name, field in RecordMetadata.model_fields.items()]
            df = pd.DataFrame(data=metadata_list, columns=columns)

            st.write("Creating CSV file...")
            df.to_csv(Path(folder_path / "metadata.csv"), index=False)

            # Also prints to the terminal running Streamlit
            st.success(f"Done! CSV created at {folder_path / 'metadata.csv'}")
        else:
            st.error(f"The folder {folder_path} does not exist or is not a directory.")