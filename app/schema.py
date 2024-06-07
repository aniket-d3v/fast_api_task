from pydantic import BaseModel,EmailStr
from typing import Optional


class Userbase(BaseModel):
    username:str
    email:EmailStr

class Usercreate(Userbase):
    password:str

class Userupdate(Userbase):
    password:Optional[str]=None

class User(BaseModel):
    id:int
    class Config():
        orm_mode=True


class Token(BaseModel):
    access_token:str
    refresh_token:str

class TokenData(BaseModel):
    username:Optional[str]=None

