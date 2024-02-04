import json
import pytest

from uuid import uuid4


async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True
    }

    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True
    }

    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] == user_data["is_active"]


async def test_update_user_by_id(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True
    }

    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "cheburek@kek.com",
    }

    await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
                {},
                422,
                {
                    "detail": "At least one parameter for user update info should be provided"
                },
        ),
        (
                {"name": "123"}, 422, {"detail": "Name should contains only letters"}
        ),
        (
                {"email": ""},
                422,
                {
                    "detail": [
                                {
                                  "type": "value_error",
                                  "loc": [
                                    "body",
                                    "email"
                                  ],
                                  "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
                                  "input": "",
                                  "ctx": {
                                    "reason": "The email address is not valid. It must have exactly one @-sign."
                                    }
                                 }
                              ]
                },
        ),
        (
                {"surname": ""},
                422,
                {
                    "detail": [
                                {
                                  "type": "string_too_short",
                                  "loc": [
                                    "body",
                                    "surname"
                                  ],
                                  "msg": "String should have at least 1 character",
                                  "input": "",
                                  "ctx": {
                                    "min_length": 1
                                  },
                                  "url": "https://errors.pydantic.dev/2.5/v/string_too_short"
                                }
                              ]
                },
        ),
        (
                {"name": ""},
                422,
                {
                    "detail": [
                                {
                                  "type": "string_too_short",
                                  "loc": [
                                    "body",
                                    "name"
                                  ],
                                  "msg": "String should have at least 1 character",
                                  "input": "",
                                  "ctx": {
                                    "min_length": 1
                                  },
                                  "url": "https://errors.pydantic.dev/2.5/v/string_too_short"
                                }
                              ]
                },
        ),
        (
                {"surname": "123"}, 422, {"detail": "Surname should contains only letters"}
        ),
        (
                {"email": "123"},
                422,
                {
                    "detail": [
                                {
                                  "type": "value_error",
                                  "loc": [
                                    "body",
                                    "email"
                                  ],
                                  "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
                                  "input": "123",
                                  "ctx": {
                                    "reason": "The email address is not valid. It must have exactly one @-sign."
                                  }
                                }
  ]
                },
        ),
    ],
)
async def test_update_user_validation_error(
        client,
        create_user_in_database,
        get_user_from_database,
        user_data_updated,
        expected_status_code,
        expected_detail,
):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True
    }

    await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail
