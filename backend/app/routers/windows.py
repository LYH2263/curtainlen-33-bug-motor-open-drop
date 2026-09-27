from fastapi import APIRouter, HTTPException
from app.repositories import history, windows as repo
router = APIRouter()
@router.get("/windows")
def list_windows(): return {"items": repo.list_windows()}
@router.get("/windows/{wid}")
def get_window(wid: int):
    r = repo.get_window(wid)
    if not r: raise HTTPException(404)
    r["last_track_run"] = history.latest_track_run_for_window(wid)
    return r
