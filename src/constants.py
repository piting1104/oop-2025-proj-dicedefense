from pygame.math import Vector2

# screen
WIDTH, HEIGHT = 500, 550

# grid
CELL_SIZE = 50
GAP = 5
MARGIN = 12
GRID_ROWS, GRID_COLS = 3, 5
GRID_POS = (WIDTH - (CELL_SIZE * GRID_COLS + GAP * (GRID_COLS - 1))) / 2

# enemy
ENEMY_SIZE = 40

# enemy path
DIST = (GRID_POS - MARGIN) / 2
LEFT_TOP = Vector2(DIST, DIST)
RIGHT_TOP = Vector2(WIDTH - DIST, DIST)
LEFT_DOWN = Vector2(DIST, DIST * 2 + CELL_SIZE * 4)
RIGHT_DOWN = Vector2(WIDTH - DIST, DIST * 2 + CELL_SIZE * 4)

# max point
MAX_POINTS = 6