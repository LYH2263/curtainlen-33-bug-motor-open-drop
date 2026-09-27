import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="curtainlen-test-")

import pytest
from fastapi import HTTPException

from app import seed
from app.config import DB_PATH
from app.modules import motor_track
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture(autouse=True)
def fresh_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    seed.init_db()
    yield


def test_track_length_sum():
    assert motor_track.track_length(3.0, 0.2, 0.2) == 3.4


def test_track_length_zero_ext():
    assert motor_track.track_length(2.2, 0, 0) == 2.2


def test_track_length_negative_raises():
    with pytest.raises(ValueError):
        motor_track.track_length(3.0, -0.1, 0.2)


def test_estimate_off_has_no_track_fields():
    r = estimate_service.run_estimate(1, 1, save=True, note="")
    assert r["meters"] == 14.25
    assert "track_length" not in r
    assert "motor_track" not in r
    run = history.get_run(r["run_id"])
    assert "track_length" not in run["result"]


def test_estimate_on_returns_track_and_same_meters():
    off = estimate_service.run_estimate(1, 1, save=False, note="")
    on = estimate_service.run_estimate(1, 1, save=True, note="",
                                       motor_track_on=True, track_ext_left=0.2, track_ext_right=0.3)
    assert on["meters"] == off["meters"]
    assert on["motor_track"] is True
    assert on["track_length"] == 3.5
    run = history.get_run(on["run_id"])
    assert run["result"]["motor_track"] is True
    assert run["result"]["track_ext_left"] == 0.2
    assert run["result"]["track_ext_right"] == 0.3
    assert run["result"]["track_length"] == 3.5
    assert run["result"]["meters"] == off["meters"]


def test_negative_ext_fails_and_no_history_row():
    before = len(history.list_runs())
    with pytest.raises(HTTPException) as ei:
        estimate_service.run_estimate(1, 1, save=True, note="",
                                      motor_track_on=True, track_ext_left=-0.1)
    assert ei.value.status_code == 422
    assert len(history.list_runs()) == before


def test_default_ext_from_settings():
    settings_repo.set_values({"default_track_ext": "0.15"})
    r = estimate_service.run_estimate(1, 1, save=False, note="", motor_track_on=True)
    assert r["track_ext_left"] == 0.15
    assert r["track_ext_right"] == 0.15
    assert r["track_length"] == 3.3


def test_settings_change_does_not_rewrite_old_runs():
    r = estimate_service.run_estimate(1, 1, save=True, note="",
                                      motor_track_on=True, track_ext_left=0.2, track_ext_right=0.2)
    settings_repo.set_values({"default_track_ext": "0.9"})
    run = history.get_run(r["run_id"])
    assert run["result"]["track_length"] == 3.4
    assert run["result"]["track_ext_left"] == 0.2


def test_latest_track_run_for_window_skips_plain_runs():
    estimate_service.run_estimate(1, 1, save=True, note="")
    t = estimate_service.run_estimate(1, 1, save=True, note="",
                                      motor_track_on=True, track_ext_left=0.1, track_ext_right=0.1)
    estimate_service.run_estimate(1, 1, save=True, note="")
    latest = history.latest_track_run_for_window(1)
    assert latest["id"] == t["run_id"]
    assert latest["result"]["track_length"] == 3.2
