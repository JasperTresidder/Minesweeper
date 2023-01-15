from .button import Button
import pygame


class Menu:
    def __init__(self, screen: pygame.Surface, kind):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.kind = kind
        self.bg_img = pygame.image.load('data/img/background.gif')
        self.bg_img = pygame.transform.scale(self.bg_img, (self.screen_size[0], self.screen_size[1]))
        if self.kind == 0:
            self.custom = Button(self.screen_size[0] / 5, self.screen_size[1] / 5, self.screen, 'Custom')
            self.beginner = Button(self.screen_size[0] / 5, 2*self.screen_size[1] / 5, self.screen, 'Beginner')
            self.intermediate = Button(self.screen_size[0] / 5, 3*self.screen_size[1] / 5, self.screen, 'Intermediate')
            self.advanced = Button(self.screen_size[0] / 5, 4 * self.screen_size[1] / 5, self.screen, 'Advanced')
            self.leaderboard = Button(2* self.screen_size[0] / 5, 4 * self.screen_size[1] / 5, self.screen, 'Leaderboard')
            self.buttons = [self.custom, self.beginner, self.intermediate, self.advanced, self.leaderboard]

        elif self.kind == 1:
            self.back = Button(self.screen_size[0] / 5, 1 * self.screen_size[1] / 10, self.screen, 'Back')
            self.buttons = [self.back]
        else:
            self.buttons = self.generate_leaderboard()
            self.back = Button(self.screen_size[0] / 5, 1 * self.screen_size[1] / 10, self.screen, 'Back')
            self.buttons.append(self.back)
        self.close = Button(4*self.screen_size[0] / 5, self.screen_size[1] / 10, self.screen, 'X')
        self.buttons.append(self.close)

    def draw(self):
        if self.kind != 1 and self.kind != 2:
            self.screen.blit(self.bg_img, (0, 0))
        for button in self.buttons:
            button.draw()

    def clicked(self, location: tuple):
        for button in self.buttons:
            if button.is_clicked(location):
                return button.name
        return None

    def generate_leaderboard(self):
        with open("data/record.txt", 'r') as file:
            data = file.readlines()
        temp = []
        buttons = []
        count = 0
        a = ['Custom', 'Beginner', 'Intermediate', 'Advanced']
        for line in data:
            if len(line) < 5:
                temp.append([])
            else:
                temp.append(sorted([float(i) for i in data[count].replace('\n', '')[3:].split(',')]))
            count += 1
        for i, arr in enumerate(temp):
            buttons.append(Button((i+1)*self.screen_size[0]/5, self.screen_size[1]/7 + 50, self.screen, a[i]))
            for j, d in enumerate(arr):
                if j < 5:
                    buttons.append(Button((i+1)*self.screen_size[0]/5, (j + 2)*self.screen_size[1]/7 + 50, self.screen, str(d)))

        return buttons
