from progress_bar import ProgressBarHandler

import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import types

def create_animation_fe_static_elasticity(local_dict):
    fig1 = local_dict['fig1']
    ax1 = local_dict['ax1']
    line2 = local_dict['line2']

    idisp = local_dict['idisp']
    nt = local_dict['nt']

    u_results = local_dict['u_results']

    animation_progress_handler = ProgressBarHandler(math.ceil(nt/idisp), "Creating animation...", remain_after_finish=False)

    def update(n, l2):
        it = n * idisp

        l2.set_ydata(u_results[n])
        
        animation_progress_handler(n)
        
        return l2, 

    return _wrap_animation_with_html5(animation.FuncAnimation(fig1, update, math.ceil(nt/idisp), fargs=(line2, ), interval=50)

def _wrap_animation_with_html5(ani):
    import types
    def _to_jshtml(self, *args, **kwargs):
        return animation.Animation.to_html5_video(self)
    ani.to_jshtml = types.MethodType(_to_jshtml, ani)
    return ani

