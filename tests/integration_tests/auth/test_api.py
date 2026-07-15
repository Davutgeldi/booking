import pytest


@pytest.mark.parametrize("first_name, last_name, email, password", [
    ("Davut", None, "dawutsh@gmail.com", "12345678"),
])
async def test_register_user(
    first_name,
    last_name,
    email,
    password,
    ac,
):
    resp_register = await ac.post(
        "/auth/register",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
    )

    assert resp_register.status_code == 200

    resp_login = await ac.post(
        "auth/login",
        json={
            "email": email,
            "password": password,
        }
    )

    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]

    resp_me = await ac.get("/auth/me")

    assert resp_me.status_code == 200

    user = resp_me.json()

    assert user["email"] == email

    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == 200
    assert "access_token" not in ac.cookies