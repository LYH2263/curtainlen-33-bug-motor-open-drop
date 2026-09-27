from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import settings_repo
router = APIRouter()

class SettingsBody(BaseModel):
    default_fullness: Optional[float] = None
    default_track_ext: Optional[float] = None

@router.get("/settings")
def settings(): return settings_repo.get_all()

@router.put("/settings")
def update_settings(body: SettingsBody):
    updates = {}
    if body.default_fullness is not None:
        updates["default_fullness"] = body.default_fullness
    if body.default_track_ext is not None:
        if body.default_track_ext < 0:
            raise HTTPException(422, "default_track_ext must be >= 0")
        updates["default_track_ext"] = body.default_track_ext
    settings_repo.set_values(updates)
    return settings_repo.get_all()
