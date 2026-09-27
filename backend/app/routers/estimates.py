from typing import Optional
from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(window_id: int = Query(...), fabric_id: int = Query(...), save: bool = False,
            motor_track: bool = False, track_ext_left: Optional[float] = None,
            track_ext_right: Optional[float] = None):
    return estimate_service.run_estimate(window_id, fabric_id, save, "",
                                         motor_track, track_ext_left, track_ext_right)
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(body.window_id, body.fabric_id, body.save, body.note,
                                         body.motor_track, body.track_ext_left, body.track_ext_right)
