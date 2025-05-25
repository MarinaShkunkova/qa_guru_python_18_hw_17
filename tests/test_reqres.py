import requests
import pytest
from jsonschema import validate

from schemas import (post_user_schema,
                     put_user_schema,
                     get_single_user_schema,
                     get_list_users_schema,
                     post_register_user_schema)

BASE_URL = "https://reqres.in/api"

ENDPOINT_CREATE = "/users"
ENDPOINT_DELETE = "/users/"
ENDPOINT_UPDATE = "/users/"
ENDPOINT_GET_USER = "/users/"
ENDPOINT_GET_LIST_USERS = "/users?page=2"
ENDPOINT_REGISTER = "/register"

USER_FOR_TESTS_DATA = {"name": "UserForTests",
                       "job": "tester"
                       }

CREATE_DATA = {"name": "Irina",
               "job": "driver"
               }
UPDATE_DATA = {"name": "Misha",
               "job": "manager"
               }

REGISTER_DATA = {"email": "eve.holt@reqres.in",
                 "password": "pistol"
                 }

REGISTER_DATA_FAILED_EMAIL = {"email": "eveholt@reqres.in",
                              "password": "pistol"
                              }

API_KEY = {"x-api-key": "reqres-free-v1"}

GET_USER_ID = "2"

GET_NO_USER_ID = "0"


@pytest.fixture(scope='function')
def create_user_for_tests():
    response = requests.post(f"{BASE_URL}{ENDPOINT_CREATE}",
                             json=USER_FOR_TESTS_DATA,
                             headers=API_KEY)
    assert response.status_code == 201, "Ошибка при создании пользователя для тестов"
    user_for_tests_data = response.json()
    return user_for_tests_data['id']


def test_update_user_data(create_user_for_tests):
    response = requests.put(f"{BASE_URL}{ENDPOINT_UPDATE}{create_user_for_tests}",
                            json=UPDATE_DATA,
                            headers=API_KEY)
    assert response.status_code == 200
    assert response.json()["name"] == UPDATE_DATA["name"]
    assert response.json()["job"] == UPDATE_DATA["job"]
    response_body = response.json()
    validate(response_body, put_user_schema)


def test_delete_user(create_user_for_tests):
    response = requests.delete(f"{BASE_URL}{ENDPOINT_CREATE}{create_user_for_tests}",
                               headers=API_KEY)
    assert response.status_code == 204
    assert response.text == ""


def test_create_user_success():
    response = requests.post(f"{BASE_URL}{ENDPOINT_CREATE}",
                             json=CREATE_DATA,
                             headers=API_KEY)
    assert response.status_code == 201
    assert response.json()["name"] == CREATE_DATA["name"]
    assert response.json()["job"] == CREATE_DATA["job"]
    response_body = response.json()
    validate(response_body, post_user_schema)


def test_get_user_success():
    response = requests.get(f"{BASE_URL}{ENDPOINT_GET_USER}{GET_USER_ID}",
                            headers=API_KEY)
    assert response.status_code == 200
    response_body = response.json()
    validate(response_body, get_single_user_schema)


def test_get_user_error():
    response = requests.get(f"{BASE_URL}{ENDPOINT_GET_USER}{GET_NO_USER_ID}",
                            headers=API_KEY)
    assert response.status_code == 404


def test_get_list_users():
    response = requests.get(f"{BASE_URL}{ENDPOINT_GET_LIST_USERS}",
                            headers=API_KEY)
    assert response.status_code == 200
    response_body = response.json()
    validate(response_body, get_list_users_schema)


def test_post_register_success():
    response = requests.post(f"{BASE_URL}{ENDPOINT_REGISTER}",
                             data=REGISTER_DATA,
                             headers=API_KEY)
    assert response.status_code == 200
    response_body = response.json()
    validate(response_body, post_register_user_schema)


def test_post_register_error():
    response = requests.post(f"{BASE_URL}{ENDPOINT_REGISTER}",
                             data=REGISTER_DATA_FAILED_EMAIL,
                             headers=API_KEY)
    assert response.status_code == 400
