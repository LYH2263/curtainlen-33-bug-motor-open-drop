"""Shape payloads for history open views (motor track length)."""

from __future__ import annotations

from copy import deepcopy


DEFAULT_TRACK_EXT = 0.2


def has_motor(result: dict) -> bool:
    return bool(result.get("motor_track")) or result.get("track_length") is not None


def open_drop_track(result: dict, dims: dict | None = None, settings: dict | None = None) -> dict:
    """Keep motor_track / track_ext_*, but drop or recompute track_length from live settings."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_motor(out):
        return out
    if not out.get("motor_track"):
        out["motor_track"] = True
    # Prefer live default_track_ext from settings when available.
    live_ext = None
    if settings is not None:
        raw = settings.get("default_track_ext")
        if raw is not None and str(raw) != "":
            try:
                live_ext = float(raw)
            except (TypeError, ValueError):
                live_ext = DEFAULT_TRACK_EXT
    width = None
    if dims:
        width = dims.get("width")
    if live_ext is not None and width is not None:
        out["track_length"] = round(float(width) + live_ext + live_ext, 3)
        out["open_motor_live_ext"] = True
    else:
        # Drop track_length while keeping motor_track and ext fields.
        out["list_track_length"] = out.get("track_length")
        out["track_length"] = None
        out["open_motor_dropped"] = True
    return out


def summarize_motor(result: dict) -> dict:
    """Flat view of motor switch / track length for open consumers."""
    if not isinstance(result, dict):
        return {}
    return {
        "motor_track": bool(result.get("motor_track")),
        "track_ext_left": result.get("track_ext_left"),
        "track_ext_right": result.get("track_ext_right"),
        "track_length": result.get("track_length"),
        "list_track_length": result.get("list_track_length"),
        "open_motor_dropped": bool(result.get("open_motor_dropped")),
        "open_motor_live_ext": bool(result.get("open_motor_live_ext")),
    }
