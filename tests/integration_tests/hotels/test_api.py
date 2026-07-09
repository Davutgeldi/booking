async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2026-07-01",
            "date_to": "2026-07-10",
        })
    assert response.status_code == 200
    print(response)