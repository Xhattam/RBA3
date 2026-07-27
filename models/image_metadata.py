from pydantic import BaseModel, Field, ValidationError, AfterValidator
import re
from typing import Annotated


def check_subject(subject, title) -> str:
    """ Subject should be a single word NOT appearing in title """
    subject = subject.lower().strip()

    if len(subject.split()) > 1:
        subject = subject[0]

    if re.search(f"\b{subject}\b", title.lower()):
        return ""
    else:
        return subject


class BaseRecord(BaseModel):
    title: str = Field(
        description="Description of the record, e.g. 'Photograph of loading bay from Old Civic Centre'")
    subject: Annotated[str, AfterValidator(check_subject)] = Field(
        description="One word tag of main object of picture, NOT included in title, to filter search on.",)


class RecordMetadata(BaseRecord):
    folder_name: str = Field(min_length=1, description="Name of the folder containing the record")
    file_name: str = Field(min_length=1, description="Name of the file, as it appears in the folder")
    creator: str | None = Field(description="Creator of the record, if known")
    description: str | None = Field(description="The size of file in MB")
    publisher: str | None = Field(description="Publisher of the record, if known")
    contributor: str | None = Field(description="Anyone who has contributed to the creation of the record if not already listed as Creator or Publisher")
    date: str | None = Field(description="Date the file was created")
    type: str | None = Field(description="Type of the record, e.g. image, drawing, photograph, etc.")
    format: str | None = Field(description="Format of the file, e.g. jpg, png, etc.")
    identifier: str = ""  # column needed, field never used
    language: str = Field(description="Language of the record if relevant, e.g. English", default="english")
    relation: str = ""  # column needed, field never used
    coverage: str = ""  # column needed, field never used
    rights: str = ""  # column needed, field never used
