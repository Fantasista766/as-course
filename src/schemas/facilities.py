from pydantic import BaseModel, ConfigDict, Field


class FacilityAdd(BaseModel):
    title: str = Field(..., min_length=2)


class Facility(FacilityAdd):
    id: int = Field(..., ge=1)

    class Config:
        from_attributes = True


class RoomFacilityAdd(BaseModel):
    room_id: int = Field(..., ge=1)
    facility_id: int = Field(..., ge=1)


class RoomFacility(RoomFacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
