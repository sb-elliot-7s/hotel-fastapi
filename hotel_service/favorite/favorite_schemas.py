from datetime import datetime
from pydantic import Field, BaseModel

from custom_object_id import ObjID


class FavoriteChangesSchema(BaseModel):
    datetime_upd: datetime
    res: str


class FavoriteSchema(BaseModel):
    id: ObjID = Field(alias='_id')
    account_id: str
    apartment_id: str
    is_favorite: bool
    datetime_added: datetime

    class Config:
        json_encoders = {
            ObjID: lambda o: str(o),
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M')
        }
