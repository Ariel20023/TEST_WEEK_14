from pydantic import BaseModel
from typing import Optional

class Weapon(BaseModel):
    weapon_id:str
    weapon_name:str
    weapon_type:str
    range_km:int
    weight_kg:float
    manufacturer: Optional[str] = None
    origin_country:str
    storage_location:str
    year_estimated:str

