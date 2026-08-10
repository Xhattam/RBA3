from pydantic import BaseModel, Field, ConfigDict


class RecordMetadata(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    folder_name : str = Field(description="Name of the folder containing the record", alias="Folder")
    file_name : str = Field(description="Name of the file, as it appears in the folder", alias="File")
    title : str = Field(
        description="Description of the record, e.g. 'Photograph of loading bay from Old Civic Centre'",
        default="", alias="Title")
    creator : str = Field(
        description="Creator of the record, if known", default="", alias="Creator")
    subject : str = Field(
        description="One word tag of main object of picture, NOT included in title, to filter search on.",
        default="", alias="Subject")
    description : str = Field(
        description="The size of file in MB", default="", alias="Description")
    publisher : str = Field(
        description="Publisher of the record, if known", default="N/A", alias="Publisher")
    contributor : str = Field(
        description="Anyone who has contributed to the creation of the record if not already Creator or Publisher",
        default="N/A", alias="Contributor")
    date : str = Field(
        description="Date the file was created, if available, otherwise, extraction time", alias="Date")
    type : str = Field(
        description="Type of the record, e.g. image, drawing, photograph, etc.",
        default='Photograph', alias="Type")
    format : str = Field(
        description="Format of the file, e.g. jpg, png, etc.",
        default="", alias="Format")
    identifier : str = Field(default="N/A", alias="Identifier")  # column needed, field never used
    source    : str = Field(description="Where the file comes from (e.g. Memory Stick)", default="", alias="Source") # metadata extraction error, if any
    language : str = Field(description="Language of the record if relevant, e.g. English", default="N/A", alias="Language")
    relation     : str = Field(default="N/A", alias="Relation")  # column needed, field never used
    coverage     : str = Field(default="N/A", alias="Coverage")  # column needed, field never used
    rights       : str = Field(default="N/A", alias="Rights")    # column needed, field never used


#print(RecordMetadata.model_json_schema())