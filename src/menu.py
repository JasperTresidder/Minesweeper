from .button import Button
import pygame


class Menu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.beginner = Button(self.screen_size[0] / 5, self.screen_size[1] / 3, self.screen, 'Beginner')
        self.intermediate = Button(self.screen_size[0] / 5, self.screen_size[1] / 2, self.screen, 'Intermediate')
        self.advanced = Button(self.screen_size[0] / 5, 2 * self.screen_size[1] / 3, self.screen, 'Advanced')
        self.buttons = [self.beginner, self.intermediate, self.advanced]

        self.bg_img = pygame.image.load('data/img/background.gif')
        self.bg_img = pygame.transform.scale(self.bg_img, (self.screen_size[0], self.screen_size[1]))

    def draw(self):
        self.screen.blit(self.bg_img,(0,0))
        self.beginner.draw()
        self.intermediate.draw()
        self.advanced.draw()

    def clicked(self, location: tuple):
        for button in self.buttons:
            if button.is_clicked(location):
                return button.name
        return None
