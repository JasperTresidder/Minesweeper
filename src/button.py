import pygame
class Button:
    def __init__(self, x, y, screen: pygame.Surface, text: str):
        self.x = x
        self.y = y
        self.height = 100
        self.width = 300
        self.screen = screen
        self.font = pygame.font.SysFont('chalkduster.ttf', 60)
        self.name = text
        self.text = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))


    def draw(self):
        r = pygame.Rect(self.x, self.y, self.width, self.height)
        r.center = (self.x, self.y)
        pygame.draw.rect(self.screen, (200, 200, 200), r, 0)
        r = pygame.Rect(self.x, self.y, self.width, self.height)
        r.center = (self.x, self.y)
        pygame.draw.rect(self.screen, (0, 0, 0), r, 8)
        self.screen.blit(self.text, self.text_rect)

    def is_clicked(self, pos):
        if self.x + self.width/2 > pos[0] > self.x - self.width/2 and self.y + self.height/2 > pos[1] > self.y - self.height/2:
            return True
