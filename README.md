Task was to create a simple web api which consists of authentication and basic crud operations

Database used was postgresql

## Total Endpoints

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/fad6bc26-0a87-40d4-9543-516789404c54/Untitled.png)

---

## User table (Model) :

```python
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,primary_key=True,index=True)
    email=Column(String,primary_key=True,index=True)
    password=Column(String,primary_key=True,index=True)

```

---

## Private Endpoints

Except login every single endpoint requires jwt token for a request to proceed 

 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/c1b7f1a1-1021-4935-a90b-1d1b2d715e49/Untitled.png)

---

### If Someone tries to request without a valid jwt token

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/67b0c0d8-adb2-41e9-a868-92094bb4e544/Untitled.png)

---

### Fast api OAuth2.0 used :

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/c22e21d7-bc1c-488f-80fe-af90187940d1/Untitled.png)

---

### After successfull jwt token validation

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/b988e4ac-cf67-46e9-944c-c7416fac0ffe/Untitled.png)

---

## Consists of `access_token` and `refresh_token`

After Successful login , it reponds with

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/871ad412-e0cb-466d-b431-bf06c5eff982/Untitled.png)

The expiration time for `refresh_token` is 7 days and for `access_token` it’s 30 minutes

So after 30 minutes the client side should request the new refresh token and at the specified endpoint i.e. `/refresh-token` and if the user has a valid token and is actually the user , he/she will get the response with a new `refresh_token` 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/4ca6cbb9-ce68-4c5a-bd04-919234e7f3e1/6f488f79-6f2b-4f99-8d64-bb3a27468715/Untitled.png)

> **Note** : All the endpoints are protected
> 

---

### The remaining operations are more clearly explained in the video which includes basic crud operations

# Thanks :)