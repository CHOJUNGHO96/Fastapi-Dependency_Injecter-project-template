import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures("delete_data")
async def test_registration(client, session):
    response = await client.post(
        url="/api/v1/auth/register",
        json={
            "user_email": "test@test.com",
            "user_id": "test",
            "user_password": "test123!",
            "user_name": "테스트유저",
        },
    )
    response_body = response.json()
    assert response.status_code == 200
    assert "access_token" in response_body.keys()


@pytest.mark.asyncio
async def test_login(client, session):
    response = await client.post(
        url="/api/v1/auth/login",
        json={"user_id": "test", "user_password": "test123!"},
    )
    response_body = response.json()
    assert response.status_code == 200
    assert "access_token" in response_body.keys()
    client.headers.update({"authorization": f"{response_body['access_token']}"})
