import numpy as np
import pyautogui
import pygame
import time
from config import *


# Функция вызова сообщения
def msg(text, title=""):
  pyautogui.alert(text, title)


# Изменение состояния клеток в зависимости от их окружения
def cells_update(screen, cells, size, with_progress=False):
  updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

  for row, col in np.ndindex(cells.shape):

    # Расчёт живих клеток вокруг определённой клетки
    alive = np.sum(cells[row - 1: row + 2, col - 1: col + 2]) - cells[row, col]

    if cells[row, col] == 0:
      color = COLOR_BG
    else:
      color =  COLOR_ALIVE_CELL

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

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.fill(COLOR_GRID)

  cells = np.zeros((60, 80))
  cells_update(screen, cells, CELL_SIZE)

  pygame.display.flip()
  pygame.display.update()

  running = False
  generations = 0
  start_time = None


  # Обработка событий нажатия клавиш
  while True:
    events = pygame.event.get()
    for event in events:

      # Обработка события выхода
      if event.type == pygame.QUIT:
        pygame.quit()
        return

      # Обработка событий нажатия клавиш клавиатуры
      elif event.type == pygame.KEYDOWN:

        # Начало симуляции / Пауза
        if event.key == pygame.K_SPACE:
          if start_time == None:
            if len(np.nonzero(cells)[0]) == 0:
              msg("Для начала симуляции необходимо задать начальные позиции клеток")
              break
            else:
              start_time = time.time()
          running = not running
          cells_update(screen, cells, CELL_SIZE)
          pygame.display.update()

        # Рестарт
        if event.key == pygame.K_r:
          cells = np.zeros((60, 80))
          generations = 0
          start_time = None
          cells_update(screen, cells, CELL_SIZE)
          pygame.display.update()
          if running:
            running = not running

        # Генерация случайных клеток
        if event.key == pygame.K_g:
          cells = np.random.randint(0, 2, (60, 80))
          generations = 0
          start_time = time.time()
          cells_update(screen, cells, CELL_SIZE)
          pygame.display.update()
          if not running:
            running = not running

        # Информация о симуляции
        if event.key == pygame.K_i:
          alive = len(np.nonzero(cells)[0])
          time_passed = "%s секунд" % round((time.time() - start_time), 3)
          msg(f"Поколений пройдено: {generations}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        # Помощь
        if event.key == pygame.K_F1:
          msg("Управление\n\nSPACE - пауза\nЛКМ - выставление клетки (во время паузы)\nR - перезапуск\nG - случайная генерация клеток\nI - просмотреть информацию о текущей симуляции", "Помощь")


      # Обработка событий нажатия клавиш мыши
      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()

        # Расстановка клеток
        if (pos[1] <= 600 and pos[0] <= 800):
          if not running:
            try:
              cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
            except IndexError:
              pass
        
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()

    screen.fill(COLOR_GRID)

    if running:
      cells = cells_update(screen, cells, CELL_SIZE, with_progress=True)
      pygame.display.update()

      generations = generations + 1

      time.sleep(0.001)
      if SLOW_MODE:
        time.sleep(0.1)
        
      if len(np.nonzero(cells)[0]) == 0:
        time_passed = "%s секунд" % round((time.time() - start_time), 3)
        msg(f"Все клетки вымерли!\n\nПоколений пройдено: {generations}\nЖивых клеток: 0\nПрошло времени: {time_passed}", "Информация")
        generations = 0
        start_time = None
        running = not running

    

# Вызов главной функции при запуске программы
if __name__ == "__main__":
  main()


# TODO:
# 
# + Добавить ГПИ:
# 
# + Пауза
# + Рестарт
# - Изменение скорости
# +- Таймер (учёт пауз)
# + Количество поколений
# 

