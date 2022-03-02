from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel): 
    id: int

class UserCreate(UserBase):
    email: str 
    pw: str

    fName: str 
    lName: str
    contactNo: Optional[str]

class User(UserBase): 
    isActive: bool 

    class Config: 
        orm_mode = True 
