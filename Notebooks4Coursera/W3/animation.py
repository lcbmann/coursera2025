from progress_bar import ProgressBarHandler

import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.animation import Animation as _BaseAnimation

if getattr(_BaseAnimation, "_coursera_original_to_jshtml", None) is None:
    _BaseAnimation._coursera_original_to_jshtml = _BaseAnimation.to_jshtml

    def _coursera_to_jshtml(self, fps=None, embed_frames=True, default_mode='loop'):
        try:
            return self.to_html5_video()
        except Exception:  # pragma: no cover - fall back if HTML5 export fails
            return _BaseAnimation._coursera_original_to_jshtml(self, fps=fps, embed_frames=embed_frames, default_mode=default_mode)

    _BaseAnimation.to_jshtml = _coursera_to_jshtml




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