from pydantic import BaseModel, ConfigDict, Field


class FacilityAddDTO(BaseModel):
    title: str = Field(..., min_length=2)


class FacilityDTO(FacilityAddDTO):
    id: int = Field(..., ge=1)

    class Config:
        from_attributes = True


class RoomFacilityAddDTO(BaseModel):
    room_id: int = Field(..., ge=1)
    facility_id: int = Field(..., ge=1)


class RoomFacilityDTO(RoomFacilityAddDTO):
    id: int

    model_config = ConfigDict(from_attributes=True)
