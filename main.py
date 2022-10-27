import numpy as np
import pyautogui
import pygame
import time
from config import *

# Функция вызова сообщения
def msg(text, title=""):
  pyautogui.alert(text, title)


# Изменение состояния клеток на поле
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
  slow_mode = False
  generation = 0
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
          generation = 0
          start_time = None
          cells_update(screen, cells, CELL_SIZE)
          pygame.display.update()
          if running:
            running = not running

        # Генерация случайных клеток
        if event.key == pygame.K_g:
          cells = np.random.randint(0, 2, (60, 80))
          generation = 0
          start_time = time.time()
          cells_update(screen, cells, CELL_SIZE)
          pygame.display.update()
          if not running:
            running = not running

        # Информация о симуляции
        if event.key == pygame.K_i:
          if start_time:
            alive = len(np.nonzero(cells)[0])
            if start_time != None and generation != 1:
              time_passed = "%s секунд" % round((time.time() - start_time), 3)
            else:
              time_passed = "0 секунд"
            msg(f"Поколение: {generation}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")
          else:
            msg("Симуляция ещё не запущена", "Информаиця")

        # Включение/выключение замедленного режима
        if event.key == pygame.K_s:
          slow_mode = not slow_mode

        # Помощь
        if event.key == pygame.K_F1:
          msg("Управление\n\nSPACE - пауза\nЛКМ - выставление клетки (во время паузы)\nR - перезапуск\nG - случайная генерация клеток\nI - просмотреть информацию о текущей симуляции\nS - включение/выключение замедленного режима", "Помощь")

      # Обработка события нажатия ЛКМ (расстановка клеток)
      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if not running:
          try:
            cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
          except IndexError: pass
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        
      # Обработка события нажатия ПКМ (удаление клеток)
      if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if not running:
          try:
            cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 0
          except IndexError: pass
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
      generation = generation + 1

      # Задержка
      if slow_mode:
        time.sleep(0.1)
      else:
        time.sleep(0.01)
        
      # Геймовер (при вымирании всех клеток)
      if len(np.nonzero(cells)[0]) == 0:
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        alive = 0
        if start_time != None and generation != 1:
          time_passed = "%s секунд" % round((time.time() - start_time), 3)
        else:
          time_passed = "0 секунд"
        msg(f"Симуляция стабилизировалась!\n(все клетки вымерли)\n\nПоколение: {generation}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        generation = 0
        start_time = None
        running = not running

      # Геймовер (при прекращении появления новых клеток)
      if np.array_equal(cells, prev_cells):
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        alive = len(np.nonzero(cells)[0])
        if start_time != None and generation != 1:
          time_passed = "%s секунд" % round((time.time() - start_time), 3)
        else:
          time_passed = "0 секунд"
        msg(f"Симуляция стабилизировалась!\n(появление новых клеток невозможно)\n\nПоколение: {generation}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        generation = 0
        start_time = None
        running = not running

      # Геймовер (при цикличном появлении новых клеток)
      if np.array_equal(cells, preprev_cells):
        cells_update(screen, cells, CELL_SIZE)
        pygame.display.update()
        alive = len(np.nonzero(cells)[0])
        if start_time != None and generation != 1:
          time_passed = "%s секунд" % round((time.time() - start_time), 3)
        else:
          time_passed = "0 секунд"
        msg(f"Симуляция стабилизировалась!\n(появление новых клеток циклично)\n\nПоколение: {generation}\nЖивых клеток: {alive}\nПрошло времени: {time_passed}", "Информация")

        generation = 0
        start_time = None
        running = not running


# Вызов главной функции при запуске программы
if __name__ == "__main__":
  main()


# TODO:
# 
# +++ Пауза
# +++ Рестарт
# +++ Текущее поколение
# +++ Геймовер при цикличном появлении клеток 
# +++ Изменение скорости
# +++ Стирание клеток в паузе
# *** Учёт пауз в таймере
# *** Пофиксить порядок в if running (увеличение поколений должно быть после проверки на геймовер)
# ??? Окна подтверждения при случайной генерации и рестарте
# --- Улучшить окна сообщений
# --- Счётчик добавленных вручную клеток (и счётчик удалённых)
# --- Подсказки при геймовере
# --- Цветовая палитра (белый/расный)
