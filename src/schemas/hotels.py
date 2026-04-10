from pydantic import BaseModel, Field

class Hotels(BaseModel):
    title: str
    location: str


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)