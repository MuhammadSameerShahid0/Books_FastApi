from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StdDetailsSchema(BaseModel):
    #region Student
    name: str = Field(alias="Name")
    email: str = Field(alias="Email")
    age : int = Field(alias="Age")
    #endregion

    #region Student_Profile
    address : str = Field(alias="Address")
    phone_number: int = Field(alias="Phone_Number")
    dob: datetime = Field(alias="Date_of_Birth")
    #endregion

    #region Book
    title: str = Field(alias="Book_Title")
    description: str = Field(alias="Book_Description")
    year: int = Field(alias="Book_Year")
    #endregion

    #region Student_Books
    AssignedAt: Optional[datetime] = Field(alias="Book_AssignedAt")
    ReturnDate: Optional[datetime] = Field(alias="Book_ReturnDate")
    Status: str = Field(alias="Status")
    #endregion

    #region Author
    author_name : str = Field(alias="Author_Name")
    bio: str = Field(alias="Author_Bio")
    nationality: str = Field(alias="Author_Nationality")
    #endregion
