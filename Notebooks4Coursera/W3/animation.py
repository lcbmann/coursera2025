from progress_bar import ProgressBarHandler

import numpy as np
import math
import tempfile
from base64 import b64encode
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def _guess_fps_from_animation(anim, fallback=20):
    """Return a best-effort FPS estimate for a Matplotlib animation."""
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
    """Convert a Matplotlib animation to an inline GIF HTML snippet."""
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


def create_animation_gaussian_analytical(local_dict):
    fig, ax1 = local_dict['fig'], local_dict['ax1']
    leg1, leg2, leg3, leg4, up1, up21, up22 = local_dict['leg1'], local_dict['leg2'], local_dict['leg3'], local_dict['leg4'], local_dict['up1'], local_dict['up21'], local_dict['up22']

    idisp = local_dict['idisp']
    nt = local_dict['nt']
    time = local_dict['time']

    isrc = local_dict['isrc']
    dx = local_dict['dx']
    dt = local_dict['dt']
    c0 = local_dict['c0']

    window = local_dict['window']
    xshift = local_dict['xshift']

    p_results = local_dict['p_results']
    seis_results = local_dict['seis_results']

    animation_progress_handler = ProgressBarHandler(math.ceil(nt/idisp), "Creating animation...", remain_after_finish=False)

    def update(n, leg1, leg2, leg3, leg4, up1, up21, up22):
        it = n * idisp

        p = p_results[n]
        seis = seis_results[n]
        
        ax1.set_title(f'Time Step (nt) = {it}')
        ax1.set_ylim(np.min(p), 1.1*np.max(p))

        ax1.set_xlim(isrc*dx+c0*it*dt-window*dx-xshift, isrc*dx+c0*it*dt+window*dx-xshift)

        up1.set_ydata(p)
        up21.set_ydata(seis)
        up22.set_data([time[it]], [seis[it]])
        
        animation_progress_handler(n)

        return leg1, leg2, leg3, leg4, up1, up21, up22

    return animation.FuncAnimation(fig, update, math.ceil(nt/idisp), fargs=(leg1, leg2, leg3, leg4, up1, up21, up22), interval=50)
    

def create_animation_gaussian(local_dict):
    fig = local_dict['fig']
    ax = local_dict['ax']
    leg1 = local_dict['leg1']
    up31 = local_dict['up31']

    idisp = local_dict['idisp']
    nt = local_dict['nt']

    isrc = local_dict['isrc']
    dx = local_dict['dx']
    dt = local_dict['dt']
    c0 = local_dict['c0']

    window = local_dict['window']
    xshift = local_dict['xshift']

    p_results = local_dict['p_results']

    animation_progress_handler = ProgressBarHandler(math.ceil(nt/idisp), "Creating animation...", remain_after_finish=False)

    def update(n, leg, up):
        it = n * idisp

        p = p_results[n]
        
        up.set_ydata(p)
        
        ax.set_ylim(-1.1*np.max(abs(p)), 1.1*np.max(abs(p)))
        ax.set_xlim(isrc*dx+c0*it*dt-window*dx-xshift, isrc*dx+c0*it*dt+window*dx-xshift)

        animation_progress_handler(n)

        return leg, up

    return animation.FuncAnimation(fig, update, math.ceil(nt/idisp), fargs=(leg1, up31), interval=50)