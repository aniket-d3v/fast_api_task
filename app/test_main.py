import pytest
from fastapi.testclient import TestClient
from app.main import app
API_KEY = "1234567abcdef"

client = TestClient(app)

# Helper function to get the access token
def get_access_token():
    response = client.post("/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    return response.json()["access_token"]


def get_refresh_token():
    response = client.post("/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    return response.json()["refresh_token"]

def test_login_invalid_informatiom():
    response = client.post("/login", data={"username": "test", "password": "w"})
    assert response.status_code == 403


def test_get_users():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response=client.get("/users",headers=headers)
    print(response.json())
    assert response.status_code==200

def test_get_users_no_token_passed():
    response=client.get("/users")
    print(response.json())
    assert response.status_code==401

def test_create_user_success():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", json={"username": "test11", "password": "test","email":"test11@gmail.com"}, headers=headers)
    assert response.status_code == 200
    assert "Message" in response.json()
    assert "data" in response.json()

def test_create_user_success_unauthorized():
    response = client.post("/users", json={"username": "test6", "password": "test","email":"test6@gmail.com"})
    assert response.status_code == 401



def test_create_user_failure():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users", json={"username": "test", "password": "test"}, headers=headers)
    assert response.status_code == 422


def test_update_user_failure():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/users/9999", json={"password": "new_password"}, headers=headers)
    assert response.status_code == 422


def test_put_user():
    access_token=get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/users/40", json={"username":"sumo","password": "new_password","email":"testsumo@gmail.com"}, headers=headers)
    assert response.status_code == 200

def test_put_user_with_no_access():
    response = client.put("/users/40", json={"username":"updatedtest","password": "new_password","email":"test5@gmail.com"})
    assert response.status_code == 401

def test_put_user_but_id_does_not_exists():
    access_token=get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/users/999", json={"username":"updatedtest","password": "new_password","email":"test5@gmail.com"}, headers=headers)
    assert response.status_code != 200

def test_delete_user():
    access_token=get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response=client.delete("/users/40",headers=headers)
    print(response.json())
    assert response.status_code==200


def test_delete_user_with_no_access_token():
    response=client.delete("/users/57")
    assert response.status_code!=200


def test_delete_user_wrong_user_id_which_doesNotExist():
    access_token=get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response=client.delete("/users/999",headers=headers)
    print(response.json())
    assert response.status_code!=200



# The below test case take the access_token and refresh_token and sends the refresh_token for verification and once done it check the authenticity

def test_refresh_token_success():
    access_token=get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    refresh_token=get_refresh_token()
    response=client.post("/refresh-token",headers=headers,json={
        "access_token":access_token,
        "refresh_token":refresh_token
    })
    assert response.status_code==200


def test_refresh_token_nothing_supplied():
    response=client.post("/refresh-token")
    assert response.status_code!=200


def test_refresh_invalid_token():
    headers = {"Authorization": f"Bearer adadadad"}
    response=client.post("/refresh-token",headers=headers,json={
        "access_token":"adad",
        "refresh_token":"adadawd"
    })
    assert response.status_code!=200


# The below test case contains valid request 

def test_api_key_endpoint_success():
    headers={"api_key":API_KEY}
    response=client.get("/apikeygetdata",headers=headers)
    assert response.status_code==200

# The below test case contains invalid api key

def test_api_key_endpoint_invalid_key():
    headers={"api_key":"123adks"}
    response=client.get("/apikeygetdata",headers=headers)
    assert response.status_code==403

# The below test case does not contain any api key

def test_api_key_endpoint_No_key():
    response=client.get("/apikeygetdata")
    assert response.status_code==403


# The below test case is just a simple get request so no much testcases can be made
def test_async_request_get_success():
    response=client.get("/asyncrequest")
    assert response.status_code==200


def test_multiple_body_success():
    response=client.post("/sendmedata",json={
  "item": {
    "itemname": "item1",
    "itemdesc": "desc",
    "itemprice": 99.99
  },
  "games": {
    "gamename": "minecraft"
  }
})
    assert response.status_code==200


#In the below testcase insufficient data is passed because pydantic validation model is used
def test_multiple_body_incompleteData():
    response=client.post("/sendmedata",json={
  "item": {
    "itemname": "item1",
    "itemdesc": "desc",
    "itemprice": 99.99
  }
})
    assert response.status_code!=200