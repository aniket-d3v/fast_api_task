from passlib.context import CryptContext

pwd_ctx=CryptContext(schemes=["bcrypt"],deprecated="auto")
hsh=pwd_ctx.hash("test1234")
