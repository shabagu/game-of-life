import pygame


class Button:
  def __init__(self, text, font, x=0, y=0):
    self.text = font.render(text, 1, pygame.Color("White"))
    self.size = self.text.get_size()
    self.surface = pygame.Surface(self.size)
    self.surface.blit(self.text, (0, 0))
    # self.surface.fill(bg)
    self.x = x
    self.y = y
    self.area = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

  def change_text(self, text, font):
    self.text = font.render(text, 1, pygame.Color("Red"))
    self.size = self.text.get_size()
    self.surface = pygame.Surface(self.size)
    self.surface.blit(self.text, (0, 0))
