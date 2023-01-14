import sys
import time

import pygame
pygame.init()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN, vsync=1)
screen_width = screen.get_width()
screen_height = screen.get_height()


from src.menu import Menu
from src.board import Board

def create_world():
    menu = Menu(screen)
    return menu


def setup(game_type: str, screen: pygame.Surface):
    # create board
    match game_type:
        case 'Beginner':
            board = Board(9, 9, 10, screen)
        case 'Intermediate':
            board = Board(16, 16, 40, screen)
        case 'Advanced':
            board = Board(24, 24, 99, screen)
    board.calculate()
    return board

def main():
    in_menu = True
    in_game = False
    after_game = False
    mode = ''
    m = create_world()
    while in_menu:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mode = m.clicked(pygame.mouse.get_pos())
                if mode is not None:
                    in_menu = False
                    in_game = True
            elif event.type == pygame.KEYDOWN:
                if event.mod and pygame.K_q:
                    sys.exit()
        m.draw()
        pygame.display.flip()

    board = setup(mode, screen)

    while in_game:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.KEYDOWN:
                if event.mod and pygame.K_q:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if board.right_click(location):
                        in_game = False
                        after_game = True
                if pygame.mouse.get_pressed()[2]:
                    board.left_click(location)

        bg_img = pygame.image.load('data/img/mw.jpg')
        bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        screen.blit(bg_img,(0,0))
        board.draw()
        pygame.display.flip()

    board.reset()
    count = 0
    while after_game:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                after_game = False
            if event.type == pygame.KEYDOWN:
                if event.mod and pygame.K_q:
                    sys.exit()

        bg_img = pygame.image.load('data/img/mw.jpg')
        bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        screen.blit(bg_img, (0, 0))
        board.draw()
        pygame.display.flip()
        if count == 120:
            after_game = False
        count += 1

if __name__ == '__main__':
    while(1):
        main()

