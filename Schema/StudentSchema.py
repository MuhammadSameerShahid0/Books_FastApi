from pydantic import BaseModel


class StudentCreate(BaseModel): # For request
    name: str
    age: int
    email: str
    IsStudent: bool

class StudentResponse(BaseModel):  # For response
    id: int
    name: str
    age: int
    email: str
    IsStudent: bool

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: str
    age: int
    email: str

class StudentDelete(BaseModel):
    id: int
    email: str