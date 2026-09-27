from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.modules import motor_track
from app.repositories import fabrics, history, settings_repo, windows

DEFAULT_TRACK_EXT = 0.2

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str,
                 motor_track_on: bool = False, track_ext_left=None, track_ext_right=None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
    record = dict(calc)
    if motor_track_on:
        default_ext = float(settings.get("default_track_ext") or DEFAULT_TRACK_EXT)
        ext_left = default_ext if track_ext_left is None else float(track_ext_left)
        ext_right = default_ext if track_ext_right is None else float(track_ext_right)
        try:
            length = motor_track.track_length(w["width"], ext_left, ext_right)
        except ValueError as e:
            raise HTTPException(422, str(e))
        record.update(motor_track=True, track_ext_left=ext_left,
                      track_ext_right=ext_right, track_length=length)
    run_id = history.insert_run(window_id, fabric_id, record, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **record}
