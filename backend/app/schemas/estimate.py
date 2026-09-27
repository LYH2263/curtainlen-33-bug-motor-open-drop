from typing import Optional
from pydantic import BaseModel

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    motor_track: bool = False
    track_ext_left: Optional[float] = None
    track_ext_right: Optional[float] = None
