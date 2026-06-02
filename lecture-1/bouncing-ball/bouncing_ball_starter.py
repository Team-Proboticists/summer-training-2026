"""
HW 2 — Bouncing Ball with Trail & Collision
============================================
Libraries: OpenCV, NumPy, Matplotlib

Fill in every section marked with  TODO  to complete the assignment.
Do NOT change function signatures or remove any existing lines.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# ── Canvas & simulation config ─────────────────────────────────────────────
WIDTH, HEIGHT = 400, 400
BALL_RADIUS   = 15
TRAIL_LEN     = 15          # keep exactly this many past positions
FPS           = 30
N_FRAMES      = 200
BALL_COLOR    = (0, 200, 255)   # BGR  — feel free to change
BG_COLOR      = (30, 30, 30)    # dark background

# ── Part A: NumPy — state initialisation ───────────────────────────────────
# TODO: create position as a float64 NumPy array, shape (2,)
#       start somewhere near the centre
position = ...

# TODO: create velocity as a float64 NumPy array, shape (2,)
#       pick any non-zero starting speed (e.g. 4 px/frame in each axis)
velocity = ...

# Trail buffer — stores past positions (filled automatically once you update position)
trail = deque(maxlen=TRAIL_LEN)


# ── Part A: update physics for one frame ───────────────────────────────────
def update_physics():
    """Move the ball and bounce off walls. Modifies global position & velocity."""
    global position, velocity

    # TODO: add velocity to position (one line, NumPy operation)


    # TODO: detect collision with LEFT or RIGHT wall
    #       condition: position[0] < BALL_RADIUS  or  position[0] > WIDTH - BALL_RADIUS
    #       action:    flip velocity[0]  and  clip position[0] into valid range


    # TODO: detect collision with TOP or BOTTOM wall  (axis 1)
    #       same idea as above but for position[1] / HEIGHT


    # record current position in trail (do this AFTER updating position)
    trail.append(position.copy())


# ── Part B: OpenCV — draw one frame ────────────────────────────────────────
def draw_frame():
    """Return a uint8 RGB image of the current frame."""

    # create blank canvas (BGR)
    canvas = np.full((HEIGHT, WIDTH, 3), BG_COLOR, dtype=np.uint8)

    # TODO: draw the trail
    #   for each (i, pos) in enumerate(trail):
    #     - compute an alpha that goes from ~0.1 (oldest) to ~0.9 (newest)
    #       hint: alpha = (i + 1) / TRAIL_LEN
    #     - compute a radius that shrinks toward the tail
    #       hint: radius = max(2, int(BALL_RADIUS * (i + 1) / TRAIL_LEN))
    #     - draw a filled circle on a *separate* overlay canvas
    #     - blend the overlay onto canvas using cv2.addWeighted()
    #       signature: cv2.addWeighted(src1, alpha, src2, 1-alpha, 0, dst)


    # TODO: draw the main ball on canvas using cv2.circle()
    #       use position (cast to int tuple), BALL_RADIUS, BALL_COLOR, thickness=-1


    # convert BGR → RGB for Matplotlib
    # TODO: return the converted frame (one line using cv2.cvtColor)
    return canvas   # ← replace this with the converted frame


# ── Part C: Matplotlib — animation ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(5, 5))
ax.axis("off")
im = ax.imshow(np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8))

def animate(frame_idx):
    update_physics()
    rgb_frame = draw_frame()
    im.set_data(rgb_frame)

    # TODO: compute speed as the L2 norm of velocity (one line, np.linalg.norm)
    speed = 0.0   # ← replace

    # TODO: set the axes title to show frame number and speed
    #       format: "frame: {frame_idx}   speed: {speed:.2f} px/frame"


    return [im]

anim = FuncAnimation(fig, animate, frames=N_FRAMES, interval=1000 // FPS, blit=True)
plt.tight_layout()
plt.show()
