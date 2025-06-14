from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int

    class Config:
        from_attributes = True


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int

    class Config:
        from_attributes = True
