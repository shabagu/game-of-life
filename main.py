import numpy as np
import pygame
import time

from Button import Button
from config import *
from events import *


# Изменение состояния клеток в зависимости от их окружения
def update(screen, cells, size, with_progress=False):
  updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

  for row, col in np.ndindex(cells.shape):
    alive = np.sum(cells[row - 1: row + 2, col - 1: col + 2]) - cells[row, col]
    color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_CELL

    if cells[row, col] == 1:

      if alive < 2 or alive > 3:
        if with_progress:
          color = COLOR_DYING_CELL

      elif 2 <= alive <= 3:
        updated_cells[row, col] = 1
        if with_progress:
          color = COLOR_ALIVE_CELL

    else:

      if alive == 3:
        updated_cells[row, col] = 1
        if with_progress:
          color = COLOR_ALIVE_CELL

    pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

  return updated_cells

# Главная функция программы
def main():
  pygame.init()
  pygame.display.set_caption('Искусстевнная жизнь')
  font = pygame.font.SysFont("Arial", 24)
  # msg("Привет!")

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.fill(COLOR_GRID)

  cells = np.zeros((60, 80))
  update(screen, cells, CELL_SIZE)

  pygame.display.flip()
  pygame.display.update()

  running = False

  # Инициирование кнопок
  
  # clock = pygame.time.Clock()
  # button = Button("Управление", font, 670, 610)
  button = Button("Управление", font, SCREEN_WIDTH - 130, SCREEN_HEIGHT - 40)
  screen.blit(button.surface, (button.x, button.y))
  pygame.display.update()
  # clock.tick(30)

  # Обработка событий нажатия клавиш и кликов
  while True:
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        pygame.quit()
        return

      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          running = not running
          update(screen, cells, CELL_SIZE)
          screen.blit(button.surface, (button.x, button.y))
          pygame.display.update()

      # elif event.type == pygame.MOUSEBUTTONDOWN:
      #   if pygame.mouse.get_pressed()[0]
      
      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()

        # Расстановка клеток
        if (pos[1] <= 600 and pos[0] <= 800):
          if not running:
            try:
              cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
            except IndexError:
              pass
        
        # Нажатие на кнопку паузы (Инфромации?)
        if button.area.collidepoint(pos[0], pos[1]):
          # if running:
          #   button.set("Пауза", font, 690, 610)
          # if not running:
          #   button.set("Симуляция", font, 690, 610)

          # screen.blit(button.surface, (button.x, button.y))
          # pygame.display.update()

          # !!!
          # running = not running

          msg("Управление\nSPACE - пауза\nЛКМ - выставление клетки (во время паузы)")
        
        update(screen, cells, CELL_SIZE)
        # pygame.display.update() # TODO: объединить в один апдейт метод
        screen.blit(button.surface, (button.x, button.y))
        pygame.display.update()

    screen.fill(COLOR_GRID)

    if running:
      cells = update(screen, cells, CELL_SIZE, with_progress=True)
      screen.blit(button.surface, (button.x, button.y))
      pygame.display.update()

      if SLOW_MODE:
        time.sleep(0.1)

    time.sleep(0.001)

# Вызов главной функции при запуске программы
if __name__ == "__main__":
  main()


# TODO:
# 
# + Добавить ГПИ:
# 
# + Пауза
# - Рестарт
# - Изменение скорости
# Кнопка случайного заполнения поля
# Таймер
# Количество поколений (?)
# 