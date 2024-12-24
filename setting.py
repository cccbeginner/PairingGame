import pygame

FPS = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CHARACTER_HEIGHT = 450

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
SNOW = (200, 200, 230)

BTN_COLORS = [RED, GREEN, YELLOW, BLUE, PURPLE]

COLOR_BTN_CD = 2

## LEVEL[i][j] means character j's data in level i
## Each stuff in data means: spawn_time(ms), sex(0,1), speed
LEVEL = [
    [
        [0, 0, 0.8],
        [3, 1, 0.8],
        [5, 1, 0.8],
        [7, 1, 0.8],
        [9, 0, 0.8],
        [10, 0, 0.8],
    ],
    [
        [0, 0, 0.8],
        [3, 1, 0.8],
        [5, 1, 0.8],
        [6, 0, 0.8],
        [7, 1, 0.8],
        [8, 1, 0.8],
        [9, 0, 0.8],
        [10, 1, 0.8],
        [15, 0, 0.8],
        [16, 0, 0.8],
    ],
    [
        [0, 1, 1],
        [2, 0, 2],
        [4, 1, 1],
        [10, 1, 5],
        [12, 0, 5],
        [14, 1, 5],
        [15, 0, 2],
        [16, 0, 2],
    ],
]
