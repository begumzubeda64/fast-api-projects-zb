from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codewithzubu'
    assert response.json()['first_name'] == 'Zubu'
    assert response.json()['last_name'] == 'Abb'
    assert response.json()['email'] == 'zubu@gmail.com'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == "8888888888"

def test_change_password_success(test_user):
    response = client.put("/users/change_password", json={"password": "Zubu@1234", "new_password": "Test@1234"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/change_password", json={"password": "Zbbu@1234", "new_password": "Test@1234"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change!'}

def test_change_phone_number_success(test_user):
    response = client.put("/users/change_phone_number", json={"phone_number": "9898989898"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

