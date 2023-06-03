

import numpy as np
import random
random.seed(7)  # ONLY HERE
np.random.seed(7)
import time # so that one can profile
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import imread
from matplotlib.patches import Rectangle

'''Cant share these unfortunately so replace with your own'''
heatmaps = np.load('./heatmaps.npy')
heatmap_scores = np.load('./heatmap_scores.npy')
background_pic = imread('./background_pic.png')

FRAMES_START = 0
FRAMES_STOP = 300
WRITE = 1
FPS = 40

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, bitrate=3600)

fig, (ax_left, ax_right) = plt.subplots(nrows=1, ncols=2, figsize=(15, 10),
                                        gridspec_kw={'width_ratios': [3, 1]})

ax_left.set_title("Pick-frequency heatmap")
ax_left.axis("off")

ax_right.axis([0, 5, 0, 50000])
ax_right.xaxis.set_visible(False)
ax_right.set_title("Total travel distance (m)")


im_ax = []  # list of drawables

im_ax.append(ax_right.add_patch(Rectangle((1, 1), 2, 6)))
im_ax.append(ax_left.imshow(background_pic, extent=[0, 200, 0, 100], alpha=0.4, zorder=2))

cmap = plt.cm.YlOrRd
im_ax.append(ax_left.imshow(heatmaps[0], extent = [0, 200, 0, 100], alpha=0.99, cmap=cmap, zorder=1))

def init():
    return im_ax

def animate(i):
    '''Bar'''
    bar = im_ax[0]
    bar.set_height(heatmap_scores[i])

    '''Heatmap'''
    im_ax[-1].remove()  # Without this, the object doesnt get properly removed
    im_ax.pop()
    prints = "i: " + str(i) + " len_mi_ax: " + str(len(im_ax))

    im_ax.append(ax_left.imshow(heatmaps[i], extent=[0, 200, 0, 100],
                                alpha=0.99, cmap=cmap, zorder=1))

    print(prints)

    return im_ax

ani = animation.FuncAnimation(fig, animate, frames=range(FRAMES_START, FRAMES_STOP),
                              blit=True, interval=1, init_func=init,
                              repeat=False)

if WRITE == 0:
    plt.show()
else:
    ani.save('./vids/vid_' + str(WRITE) + '.mp4', writer=writer)



