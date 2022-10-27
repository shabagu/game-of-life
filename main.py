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

  # Инициализация массива клеток поля
  updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

  # Обработка каждой клетки поля
  for row, col in np.ndindex(cells.shape):

    # Расчёт живих клеток вокруг определённой клетки
    alive = np.sum(cells[row - 1: row + 2, col - 1: col + 2]) - cells[row, col]

    # Первичная обработка клеток поля
    if cells[row, col] == 0:
      # Инициализация пустых клеток
      # (на этом этапе происходит вымирание клетки от одиночества)
      color = COLOR_BG
    else:
      # Инициализация не пустых клеток
      color =  COLOR_ALIVE_CELL

    # Обработка заполненных клеток поля
    if cells[row, col] == 1:

      # Вымирание клетки от перенаселения
      if alive < 2 or alive > 3:
        if with_progress:
          color = COLOR_DYING_CELL

      # Клетка выживает
      elif 2 <= alive <= 3:
        updated_cells[row, col] = 1
        if with_progress:
          color = COLOR_ALIVE_CELL

    # Зарождение жизни (при наличии трёх соседей)
    else:
      if alive == 3:
        updated_cells[row, col] = 1
        if with_progress:
          color = COLOR_ALIVE_CELL

    # Отрисовка клеток на экране pygame
    pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

  return updated_cells


# Главная функция программы
def main():

  # Инициализирование перед запуском первой симуляции
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
  prev_cells = np.zeros((60, 80))
  preprev_cells = np.zeros((60, 80))



  # Основный цикл симуляции
  while True:

    # Обработка событий нажатия клавиш
    for event in pygame.event.get():

      # Обработка события закрытия окна программы
      if event.type == pygame.QUIT:
        pygame.quit()
        return

      # Обработка событий нажатия клавиш клавиатуры
      elif event.type == pygame.KEYDOWN:

        # Начало симуляции / Пауза
        if event.key == pygame.K_SPACE:
          if start_time == None:
            if len(np.nonzero(cells)[0]) == 0:
              msg("Для начала симуляции необходимо задать начальные позиции клеток", "Информация")
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
          if start_time:
            alive = len(np.nonzero(cells)[0])
            time_passed = "%s секунд" % round((time.time() - start_time), 3)
            msg(f"Поколений пройдено: {generations}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")
          else:
            msg("Симуляция ещё не запущена", "Информаиця")

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

    # События симуляции
    if running:

      # Задание массива клеток предыдущих поколений
      preprev_cells = prev_cells
      prev_cells = cells

      # Смена поколения клеток
      cells = cells_update(screen, cells, CELL_SIZE, with_progress=True)
      pygame.display.update()

      # Счётчик поколений текущей симуляции
      generations = generations + 1

      # Задержка
      if SLOW_MODE:
        time.sleep(0.1)
      else:
        time.sleep(0.01)
        
      # Геймовер (при вымирании всех клеток)
      if len(np.nonzero(cells)[0]) == 0:
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        alive = 0
        time_passed = "%s секунд" % round((time.time() - start_time), 3)
        msg(f"Симуляция прекращена!\n(все клетки вымерли)\n\nПоколений пройдено: {generations}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        generations = 0
        start_time = None
        running = not running

      # Геймовер (при прекращении появления новых клеток)
      if np.array_equal(cells, prev_cells):
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        alive = len(np.nonzero(cells)[0])
        time_passed = "%s секунд" % round((time.time() - start_time), 3)
        msg(f"Симуляция стабилизировалась!\n(появление новых клеток невозможно)\n\nПоколений пройдено: {generations}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        generations = 0
        start_time = None
        running = not running

      # Геймовер (при цикличном появлении новых клеток)
      if np.array_equal(cells, preprev_cells):
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        alive = len(np.nonzero(cells)[0])
        time_passed = "%s секунд" % round((time.time() - start_time), 3)
        msg(f"Симуляция стабилизировалась!\n(появление новых клеток циклично)\n\nПоколений пройдено: {generations}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        generations = 0
        start_time = None
        running = not running


# Вызов главной функции при запуске программы
if __name__ == "__main__":
  main()


# TODO:
# 
# + Пауза
# + Рестарт
# + Количество поколений
# - Учёт пауз в таймере
# - Изменение скорости
# ? 
# ? Окна подтверждения при случайной генерации и рестарте
# - Улучшить окна сообщений
# - Геймовер при цикличном появлении клеток 
# - Пофиксить порядок в if running (увеличение поколений должно быть после проверки на геймовер)

