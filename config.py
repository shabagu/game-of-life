# # Чёрный/Белый (стандартная цветовая палитра)
# COLOR_BG = (10, 10, 10)
# COLOR_GRID = (40, 40, 40)
# COLOR_DYING_CELL = (170, 170, 170)
# COLOR_ALIVE_CELL = (255, 255, 255)

# # Чёрный/Красный
# COLOR_BG = (10, 10, 10)
# COLOR_GRID = (40, 40, 40)
# COLOR_DYING_CELL = (170, 0, 0)
# COLOR_ALIVE_CELL = (255, 0, 0)

# # Чёрный/Зелёный
# COLOR_BG = (10, 10, 10)
# COLOR_GRID = (40, 40, 40)
# COLOR_DYING_CELL = (0, 170, 0)
# COLOR_ALIVE_CELL = (0, 255, 0)

# # Чёрный/Синий
# COLOR_BG = (10, 10, 10)
# COLOR_GRID = (40, 40, 40)
# COLOR_DYING_CELL = (0, 0, 170)
# COLOR_ALIVE_CELL = (0, 0, 255)

# Словарь цветовых стилей
COLORS = dict(
  BLACK_WHITE = dict(
    GRID = (40, 40, 40),
    DEAD = (10, 10, 10),
    DYING = (170, 170, 170),
    ALIVE = (255, 255, 255),
  ),
  BLACK_RED = dict(
    GRID = (40, 40, 40),
    DEAD = (10, 10, 10),
    DYING = (170, 0, 0),
    ALIVE = (255, 0, 0),
  ),
  BLACK_GREEN = dict(
    GRID = (40, 40, 40),
    DEAD = (10, 10, 10),
    DYING = (0, 170, 0),
    ALIVE = (0, 255, 0),
  ),
  BLACK_BLUE = dict(
    GRID = (40, 40, 40),
    DEAD = (10, 10, 10),
    DYING = (0, 0, 170),
    ALIVE = (0, 0, 255),
  ),
  WHITE_BLACK = dict(
    GRID = (200, 200, 200),
    DEAD = (250, 250, 250),
    DYING = (80, 80, 80),
    ALIVE = (0, 0, 0),
  ),
  WHITE_RED = dict(
    GRID = (200, 200, 200),
    DEAD = (250, 250, 250),
    DYING = (170, 0, 0),
    ALIVE = (255, 0, 0),
  ),
  WHITE_GREEN = dict(
    GRID = (200, 200, 200),
    DEAD = (250, 250, 250),
    DYING = (0, 170, 0),
    ALIVE = (0, 255, 0),
  ),
  WHITE_BLUE = dict(
    GRID = (200, 200, 200),
    DEAD = (250, 250, 250),
    DYING = (0, 0, 170),
    ALIVE = (0, 0, 255),
  ),
)


# Размер клеток и экрана
CELL_SIZE = 12
SCREEN_WIDTH = CELL_SIZE * 80
SCREEN_HEIGHT = CELL_SIZE * 60
