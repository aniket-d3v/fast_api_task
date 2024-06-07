from sqlalchemy.orm import Session
from . import models,schema
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from typing import Optional
pwd_ctx=CryptContext(schemes=["bcrypt"],deprecated="auto")
ALGORITHM="HS256"
TOKEN_SECRET="a2e7d9f13508cf22a2ab280bedaa9828"
REFRESH_TOKEN_SECRET="a2e7d9f13508cf22a2ab280bedee9828"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def get_all_users(db:Session):
    users=db.query(models.User).all()
    return users

def hash_pass(password:str):
    return pwd_ctx.hash(password)


def verify_password(hashed_pass,current_password):
    verification=pwd_ctx.verify(current_password,hashed_pass)
    if not verification:
        return False
    return True

def get_current_user(db:Session,user_id:int):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        return False
    return db_user

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode=data.copy()
    if expires_delta:
        expires=datetime.utcnow()+expires_delta
    else:
        expires=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires})
    encoded_data=jwt.encode(to_encode,TOKEN_SECRET,algorithm=ALGORITHM)

    return encoded_data



def create_refresh_token(data:dict):
    expires=datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode=data.copy()
    to_encode.update({"exp":expires})
    encode_data=jwt.encode(to_encode,REFRESH_TOKEN_SECRET,algorithm=ALGORITHM)
    return encode_data

def decode_token(token:str):
    try:
        payload=jwt.decode(token,TOKEN_SECRET,algorithms=ALGORITHM)
        if payload:
            return payload
    except JWTError as e:
        print(f"Error decoding token: {e}")
        return None
def refresh_decode_token(token:str):
    try:
        payload=jwt.decode(token,REFRESH_TOKEN_SECRET,algorithms=ALGORITHM)
        if payload:
            return payload
    except JWTError as e:
        print(f"Error decoding token: {e}")
        return None


def create_new_user(db:Session,data:schema.Usercreate):
    data_dict = data.dict()
    data_dict['password'] = hash_pass(data_dict['password']) 
    new_user=models.User(**data_dict)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        return False
    finally:
        return True

def delete_user(db:Session,user_id:int):
    db_user=db.query(models.User).filter(models.User.id==user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return False
    

def update_user(db:Session,user_id:int,data:schema.Userupdate):
    db_update=db.query(models.User).filter(models.User.id==user_id).first()
    data_dict = data.dict()
    data_dict['password'] = hash_pass(data_dict['password']) 
    if db_update:
        for key,value in data_dict.items():
            setattr(db_update,key,value)
        db.commit()
        return True
    else:
        return False


