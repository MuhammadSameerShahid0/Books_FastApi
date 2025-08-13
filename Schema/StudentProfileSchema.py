from pydantic import BaseModel, Field

class UpdateProfile(BaseModel):
    student_id: int = Field(alias="StudentId")
    address : str
    phone_number : int = Field(alias="PhoneNumber")
    dob : str = Field(alias="Date_of_Birth")