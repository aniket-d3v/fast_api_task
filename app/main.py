from fastapi import FastAPI,Depends,HTTPException,Security,Body
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from . import database,models,operations,schema
from sqlalchemy.orm import Session
from jose import JWTError
from .database import SessionLocal
import requests
import time
from fastapi.concurrency import run_in_threadpool
from fastapi.security.api_key import APIKeyHeader,APIKey



oauth_scheme=OAuth2PasswordBearer(tokenUrl="login")
pwd_ctx=CryptContext(schemes=["bcrypt"],deprecated="auto")


API_KEY = "1234567abcdef"
API_KEY_NAME = "api_key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid Api key :)")


ALGORITHM="HS256"
TOKEN_SECRET="a2e7d9f13508cf22a2ab280bedaa9828"

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ignore this function :)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    payload = operations.decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user




app=FastAPI()

@app.get('/users')
async def getusers(db:Session=Depends(get_db),token:str=Depends(oauth_scheme)):
    try:
        payload=operations.decode_token(token)
        username:str=payload.get('sub')
        if not username:
            raise HTTPException(status_code=401,detail="invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")
    finally:
        all_users= operations.get_all_users(db=db)
        if not all_users:
            return {"message":"Something went wrong"}
        return all_users


@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.username == form_data.username).first()
    if not db_user or not operations.verify_password(hashed_pass=db_user.password ,current_password=form_data.password):
        raise HTTPException(status_code=401,detail="Unauthorized")
    access_token=operations.create_access_token(data={"sub":form_data.username})
    refresh_token=operations.create_refresh_token(data={"sub":form_data.username})
    return {"access_token":access_token,"token_type":"bearer","refresh_token":refresh_token}



@app.post("/refresh-token")
def refresh_token(data:schema.Token,token:str=Depends(oauth_scheme)):
    try:
        payload=operations.decode_token(token)
        if not payload:
            raise HTTPException(status_code=401,detail="invalid token")
        username:str=payload.get('sub')
        if not username:
            raise HTTPException(status_code=401,detail="invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")
    finally:
        verify_refresh=operations.refresh_decode_token(data.refresh_token)
        if not verify_refresh:
            raise HTTPException(status_code=401,detail="invalid token")

        username:str=verify_refresh.get('sub')
        if not username:
            raise HTTPException(status_code=401,detail="invalid token")
        new_accesstoken=operations.create_access_token(data={"sub":username})
        return {"new access token":new_accesstoken,"token type":"bearer"}

@app.post("/users")
def create_user(data:schema.Usercreate,db:Session=Depends(get_db),token:str=Depends(oauth_scheme)):
    try:
        payload=operations.decode_token(token)
        username:str=payload.get('sub')
        if not username:
            raise HTTPException(status_code=401,detail="invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")
    finally:
        usr=db.query(models.User).filter(models.User.username==data.username).first()
        if not usr:
            create_usr=operations.create_new_user(data=data,db=db)
            if create_usr:
                return {"Message":"Operation Successfull","data":create_usr}
            raise HTTPException(status_code=401,detail="cannot create User")
        else:
            raise HTTPException(status_code=203,detail="User already exists")
    


@app.put("/users/{user_id}")
def update_user(user_id:int,user_data:schema.Userupdate,db:Session=Depends(get_db),token:str=Depends(oauth_scheme)):
    try:
        payload=operations.decode_token(token)
        username:str=payload.get('sub')
        if not username:
            raise HTTPException(status_code=401,detail="invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")
    finally:
        usr=db.query(models.User).filter(models.User.id==user_id).first()
        if usr:
            update_usr=operations.update_user(user_id=user_id,data=user_data,db=db)
            if update_usr:
                return {"message":"Update Successfull"}
            else:
                raise HTTPException(status_code=204,detail="Some error occured")
                
        else:
            raise HTTPException(status_code=404,detail="Not found")
    

@app.delete("/users")
def delete_user(user_id:int,db:Session=Depends(get_db),token:str=Depends(oauth_scheme)):
    try:
        payload=operations.decode_token(token)
        username:str=payload.get('sub')
        if not username:
            raise HTTPException(status_code=401,detail="invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")
    finally:
        del_usr=operations.delete_user(user_id=user_id,db=db)
        if del_usr:
            return {"Message":"Deleted Successfully"}
        else:
            raise HTTPException(status_code=402,detail="Cannot delete or invalid id sent to delete that does not exist")


# The below code is not the part of the task , it showcases the developers notes mentioned

@app.get("/apikeygetdata")
def apikeywith(api_key:APIKey=Depends(get_api_key),):
    data=requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return data.json()


@app.get("/asyncrequest")
async def asyncreq():

    def fetchData():
        req=requests.get("https://jsonplaceholder.typicode.com/todos")
        if req.status_code!=200:
            raise HTTPException(status_code=req.status_code,detail="Error in getting the data")
        return req.json()
    
    data=await run_in_threadpool(fetchData)
    return data


# Multiple bodies for single endpoints

@app.post("/sendmedata")
def sendata(item:schema.Item=Body(...),games:schema.Games=Body(...)):
    return {"items":item,"games":games}
