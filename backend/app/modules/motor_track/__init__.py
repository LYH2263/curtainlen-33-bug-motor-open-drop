"""Motor track (电动轨): track length = window width + left/right extensions."""


def track_length(window_w: float, ext_left: float, ext_right: float) -> float:
    ext_left = float(ext_left)
    ext_right = float(ext_right)
    if ext_left < 0 or ext_right < 0:
        raise ValueError("track extension must be >= 0")
    return round(float(window_w) + ext_left + ext_right, 3)
