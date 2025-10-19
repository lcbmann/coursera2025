from progress_bar import ProgressBarHandler

import numpy as np
import math
import tempfile
from base64 import b64encode
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def _guess_fps_from_animation(anim, fallback=20):
    event_source = getattr(anim, "event_source", None)
    interval = getattr(event_source, "interval", None)
    if interval in (0, None):
        return fallback
    try:
        fps = max(int(round(1000.0 / interval)), 1)
    except Exception:
        fps = fallback
    return fps


def _animation_to_embedded_gif(anim, fps=None):
    target_fps = fps or _guess_fps_from_animation(anim)
    writer = animation.PillowWriter(fps=target_fps)
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        anim.save(tmp_path, writer=writer)
        data = tmp_path.read_bytes()
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except FileNotFoundError:
            pass
    encoded = b64encode(data).decode("ascii")
    return (
        "<div class='matplotlib-animation-gif' "
        "style=\"max-width: 100%; display: inline-block;\">"
        f"<img src='data:image/gif;base64,{encoded}' "
        "style=\"width: 100%; height: auto;\"/>"
        "</div>"
    )


if not hasattr(animation.Animation, "_original_to_jshtml"):
    animation.Animation._original_to_jshtml = animation.Animation.to_jshtml

    def _safe_to_jshtml(self, fps=None, embed_frames=True, default_mode=None):
        return _animation_to_embedded_gif(self, fps=fps)

    animation.Animation.to_jshtml = _safe_to_jshtml

def create_animation_fe_elastic_1d_solution(local_dict):
    fig1 = local_dict['fig1']
    ax1 = local_dict['ax1']
    line1 = local_dict['line1']
    line2 = local_dict['line2']

    idisp = local_dict['idisp']
    nt = local_dict['nt']

    u_results = local_dict['u_results']
    p_results = local_dict['p_results']

    animation_progress_handler = ProgressBarHandler(math.ceil(nt/idisp), "Creating animation...", remain_after_finish=False)

    y_min = min(np.min(u_results), np.min(p_results))
    y_max = max(np.max(u_results), np.max(p_results))
    y_diff = y_max - y_min

    y_min = y_min - y_diff * 0.1
    y_max = y_max + y_diff * 0.1

    ax1.set_ylim(y_min, y_max)
    
    def update(n, l1, l2):
        global ylim_min, ylim_max
        
        it = n * idisp

        l1.set_ydata(u_results[n])
        l2.set_ydata(p_results[n])
        
        animation_progress_handler(n)
        
        return l1, l2 

    return animation.FuncAnimation(fig1, update, math.ceil(nt/idisp), fargs=(line1, line2, ), interval=50)