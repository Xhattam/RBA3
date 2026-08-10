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
            st.write("Extracting image metadata...")
            for image_file in image_files:
                img_meta = extract_with_pillow(image_file)
                metadata_list.append(img_meta)
                st.write(f"Image: {image_file}")
            columns = [field.alias or field_name for field_name, field in RecordMetadata.model_fields.items()]
            df = pd.DataFrame(data=metadata_list, columns=columns)
            df['File'] = df['File'].astype(str)

            st.code("Creating CSV file...")
            df.to_csv(Path(folder_path / "metadata.csv"), index=False)

            # Also prints to the terminal running Streamlit
            st.code(f"Done! CSV created at {folder_path / 'metadata.csv'}")
        else:
            st.error("The folder does not exist or is not a directory.")