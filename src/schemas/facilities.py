from pydantic import BaseModel, ConfigDict, Field


class FacilityAdd(BaseModel):
    title: str = Field(..., min_length=2)


class Facility(FacilityAdd):
    id: int

    class Config:
        from_attributes = True


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
