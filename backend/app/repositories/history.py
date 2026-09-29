import json
from datetime import datetime, timezone
from app.db import connect

def insert_run(window_id, fabric_id, result, note=""):
    c = connect()
    try:
        cur = c.execute(
            "INSERT INTO calc_runs(window_id,fabric_id,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (window_id, fabric_id, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        c.commit()
        return int(cur.lastrowid)
    finally:
        c.close()

def _with_names(where="", order="ORDER BY r.id DESC"):
    return f"""SELECT r.*, w.name window_name, f.name fabric_name,
                   w.width window_width, w.height window_height, w.fullness window_fullness,
                   f.fabric_width fabric_width, f.hem_top hem_top, f.hem_bottom hem_bottom
            FROM calc_runs r
            LEFT JOIN windows w ON w.id=r.window_id LEFT JOIN fabrics f ON f.id=r.fabric_id
            {where} {order}"""

def _parse(row):
    # Read path returns the written snapshot verbatim: track_length, extensions
    # and meters are pinned at save time and must never be recomputed from
    # current settings (changing default_track_ext only affects new runs).
    d = dict(row)
    d["result"] = json.loads(d.pop("result_json"))
    return d

def list_runs(limit=50):
    c = connect()
    try:
        rows = c.execute(_with_names() + " LIMIT ?", (limit,)).fetchall()
        return [_parse(row) for row in rows]
    finally:
        c.close()

def get_run(run_id):
    c = connect()
    try:
        row = c.execute(_with_names("WHERE r.id=?"), (run_id,)).fetchone()
        return _parse(row) if row else None
    finally:
        c.close()

def latest_track_run_for_window(window_id):
    c = connect()
    try:
        row = c.execute(
            _with_names("WHERE r.window_id=? AND r.result_json LIKE '%\"track_length\"%'") + " LIMIT 1",
            (window_id,)).fetchone()
        return _parse(row) if row else None
    finally:
        c.close()
