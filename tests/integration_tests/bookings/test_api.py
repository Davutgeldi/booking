async def test_add_booking(db, authenticated_ac):
    room_id = (db.rooms.get_all())[0].id
    print(room_id)
    response = await authenticated_ac.post(
        "/bookings", 
        json={
            "room_id": room_id,
            "date_from": "2026-07-08",
            "date_to": "2026-07-11",
        }
    )
    assert response.status_code == 200

    res = response.json()

    assert res["status"] == "Successfully added"

    assert "data" in res