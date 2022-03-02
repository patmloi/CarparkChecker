from typing import Optional
from pydantic import BaseModel

class userBase(BaseModel): 
    id: int

class userCreate(userBase):
    email: str 
    pw: str

    fName: str 
    lName: str
    contactNo: Optional[str]

class user(userBase): 
    isActive: bool 

    class Config: 
        orm_mode = True 
