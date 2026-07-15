import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-07-08", "2026-07-15", 200),
    (1, "2026-07-08", "2026-07-15", 200),
    (1, "2026-07-08", "2026-07-15", 200),
    (1, "2026-07-08", "2026-07-15", 200),
    (1, "2026-07-08", "2026-07-15", 200),
    (1, "2026-07-08", "2026-07-15", 409),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    db, authenticated_user,
):
    #room_id = (db.rooms.get_all())[0].id
    print(room_id)
    response = await authenticated_user.post(
        "/bookings", 
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    res = response.json()

    assert response.status_code == status_code

    if status_code == 200:
        assert res["status"] == "Successfully added"
        assert "data" in res
        assert res["data"] is not None

    elif status_code == 409:
        assert "detail" in res
        assert res["detail"] == "Rooms are not available"


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, rooms_booked", [
    (1, "2026-07-08", "2026-07-15", 1),
    (1, "2026-07-08", "2026-07-15", 2),
    (1, "2026-07-08", "2026-07-15", 3),
])
async def test_add_and_get_booking(
    room_id,
    date_from, 
    date_to, 
    rooms_booked,
    delete_all_bookings,
    authenticated_user,
):
    response = await authenticated_user.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == 200

    response_my_bookings = await authenticated_user.get("/bookings/me")

    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == rooms_booked