from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int

    class Config:
        from_attributes = True
