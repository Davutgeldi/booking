from datetime import date

from src.schemas.bookings import BookingsAdd, BookingsPatch


async def test_crud_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=7, day=3),
        date_to=date(year=2026, month=7, day=10),
        price=69.99,
    )
    await db.bookings.add(booking)

    await db.bookings.get_one_or_none(id=1)

    update_booking = BookingsPatch(
        room_id=room_id,
        date_from=date(year=2026, month=6, day=15),
        date_to=date(year=2026, month=6, day=22),
        price=79.99,
    )

    await db.bookings.edit(update_booking, id=1)
    
    partially_edit_booking = BookingsPatch(
        date_from=date(year=2026, month=7, day=29),
        price=99.99,
    )

    await db.bookings.edit(partially_edit_booking, is_patch=True, id=1)

    await db.bookings.delete(id=1)

    await db.commit()