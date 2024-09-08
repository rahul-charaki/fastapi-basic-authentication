from datetime import datetime
from typing import  Optional
from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    id: int
    username:str
    is_active:bool
   
    class Config():
        orm_mode = True

class NewUser(BaseModel):
    username:str
    password:str
    
    class Config():
        orm_mode = True  


class ShowUser(BaseModel):
    id: int
    username: str
    is_active: Optional[bool] = None
    created_date: datetime

    class Config():
        orm_mode = True

class UpdateUser(BaseModel):
    username: str
    is_active: Optional[bool] = None
    
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
