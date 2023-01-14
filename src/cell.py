import pygame

class Cell:
    def __init__(self, x, y, cols):
        self.location = dict(x=x, y=y)
        self.bomb = False
        self.number = -1
        self.revealed = False
        self.flagged = False
        self.size = 30
        self.cols = cols

    def clicked(self, location):
        if self.location['x'] == location[0] and self.location['y'] == location[1]:
            return True

    def neighbours(self):
        n = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                x_loc = self.location['x'] + x
                y_loc = self.location['y'] + y
                if self.cols > x_loc > -1 and self.cols > y_loc > -1:
                    if not (y == 0 and x == 0):
                        n.append((x_loc, y_loc))
        return n

    def draw(self, dx, dy, screen):
        if self.revealed:
            match self.number:
                case -2:
                    img = pygame.image.load("data/img/bombdeath.gif")
                case -1:
                    img = pygame.image.load("data/img/bombrevealed.gif")
                case 0:
                    img = pygame.image.load("data/img/openblank.gif")
                case 1:
                    img = pygame.image.load("data/img/open1.gif")
                case 2:
                    img = pygame.image.load("data/img/open2.gif")
                case 3:
                    img = pygame.image.load("data/img/open3.gif")
                case 4:
                    img = pygame.image.load("data/img/open4.gif")
                case 5:
                    img = pygame.image.load("data/img/open5.gif")
                case 6:
                    img = pygame.image.load("data/img/open6.gif")
                case 7:
                    img = pygame.image.load("data/img/open7.gif")
                case 8:
                    img = pygame.image.load("data/img/open8.gif")
                case other:
                    raise NotImplemented

            img = pygame.transform.scale(img, (self.size, self.size))
            screen.blit(img, (self.location['x'] * self.size + dx, self.location['y'] * self.size + dy))
        else:
            if not self.flagged:
                img = pygame.image.load("data/img/blank.gif")
                img = pygame.transform.scale(img,(self.size, self.size))
                screen.blit(img, (self.location['x']*self.size + dx, self.location['y']*self.size + dy))
            else:
                img = pygame.image.load("data/img/bombflagged.gif")
                img = pygame.transform.scale(img, (self.size, self.size))
                screen.blit(img, (self.location['x'] * self.size + dx, self.location['y'] * self.size + dy))





