from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel): 
    email: str 
    fName: str 
    lName: str
    contactNo: Optional[str]

class UserCreate(UserBase):
    hashedPw: str


class User(UserBase): 
    id: int
    isActive: bool 

    class Config: 
        orm_mode = True 
