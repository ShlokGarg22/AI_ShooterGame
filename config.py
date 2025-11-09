# config.py
# ----------------------------------------------------------
# This file stores all configurable constants for the game.
# It helps you keep your code clean and consistent across modules.
# Example: instead of hardcoding width=960 everywhere,
#          you just import WIDTH from config.
# ----------------------------------------------------------

# ----- WINDOW SETTINGS -----
WIDTH = 960          # Width of the game window (pixels)
HEIGHT = 540         # Height of the game window (pixels)
FPS = 60             # Frames per second (how fast the game updates)
TITLE = "💀 Death Circuit - Pixel Arena"  # Window title

# ----- COLORS (RGB FORMAT) -----
# RGB = (Red, Green, Blue), each from 0 to 255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 80, 80)
CYAN = (80, 200, 255)
YELLOW = (255, 220, 120)
GREY = (60, 60, 70)

# ----- PLAYER SETTINGS -----
PLAYER_SPEED = 3.0               # Movement speed (pixels per frame)
PLAYER_SCALE = 2                 # Scaling multiplier for pixel sprite
PLAYER_FIRE_COOLDOWN = 200       # Minimum time between shots (ms)

# ----- BULLET SETTINGS -----
BULLET_SPEED = 9                 # How fast bullets move (pixels per frame)
BULLET_LIFETIME = 1000           # How long bullets exist before disappearing (ms)
BULLET_SCALE = 2                 # Scale for bullet sprite (same as player)

# ----- ENEMY SETTINGS -----
ENEMY_BASE_SPEED = 1.5           # Base speed of AI enemies
ENEMY_SCALE = 2                  # Scaling for enemy sprites
ENEMY_HP = 40                    # Base health (each enemy can have more later)

# ----- GAMEPLAY SETTINGS -----
SCORE_PER_KILL = 10              # Points per enemy kill
TILE_SIZE = 32                   # Base tile size for the arena grid

# ----------------------------------------------------------
# Why we keep this file:
# - Makes tuning easier (you can balance gameplay by changing one number)
# - Keeps all modules consistent (import once, use everywhere)
# - Avoids magic numbers scattered through the code
# ----------------------------------------------------------
