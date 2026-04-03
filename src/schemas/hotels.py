from pydantic import BaseModel

class HotelsBase(BaseModel):
    title: str
    location: str
    