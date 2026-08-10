from pydantic import BaseModel, Field


class RecordMetadata(BaseModel):
    title        : str = Field(
        description="Description of the record, e.g. 'Photograph of loading bay from Old Civic Centre'",
        default="")
    subject      : str = Field(
        description="One word tag of main object of picture, NOT included in title, to filter search on.",
        default="")
    folder_name  : str = Field(min_length=1, description="Name of the folder containing the record")
    file_name    : str = Field(min_length=1, description="Name of the file, as it appears in the folder")
    language     : str = Field(description="Language of the record if relevant, e.g. English", default="english")
    creator      : str = Field(
        description="Creator of the record, if known", default="")
    description  : str = Field(
        description="The size of file in MB", default="")
    publisher    : str = Field(
        description="Publisher of the record, if known", default="")
    contributor  : str = Field(
        description="Anyone who has contributed to the creation of the record if not already Creator or Publisher",
        default=""
    )
    date         : str = Field(
        description="Date the file was created, if available, otherwise, extraction time")
    type         : str = Field(
        description="Type of the record, e.g. image, drawing, photograph, etc.",
        default='photograph')
    format       : str = Field(
        description="Format of the file, e.g. jpg, png, etc.",
        default="")
    identifier   : str = ""  # column needed, field never used
    relation     : str = ""  # column needed, field never used
    coverage     : str = ""  # column needed, field never used
    rights       : str = ""  # column needed, field never used
    error        : str = ""  # metadata extraction error, if any


print(RecordMetadata.model_json_schema())