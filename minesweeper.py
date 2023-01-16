import sys
import time
import timeit
import pygame
pygame.init()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN, vsync=1)
screen_width = screen.get_width()
screen_height = screen.get_height()


from src.menu import Menu
from src.board import Board

font = pygame.font.SysFont('chalkduster.ttf', 60)

def create_world():
    menu = Menu(screen, 0)
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
        case 'Custom':
            # w = int(input('Width: '))
            # h = int(input('Height: '))
            # m = int(input('Mines: '))
            board = Board(50, 20, 130, screen)
        case 'Leaderboard':
            return False
        case other:
            sys.exit()

    board.calculate()
    return board

def main():
    in_menu = True
    in_game = False
    after_game = False
    won = False
    record = False
    first_game = False
    mode = ''
    m = create_world()
    with open('data/record.txt', 'r') as file:
        # read a list of lines into data
        data = file.readlines()
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
    if board == False: # leaderboard
        menu2 = Menu(screen, 2)
        in_menu = True
        while(in_menu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_menu = False
                    in_game = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    mode = menu2.clicked(pygame.mouse.get_pos())
                    if mode == 'Back':
                        in_menu = False
                        in_game = False
                        after_game = False
                    if mode == 'X':
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.mod and pygame.K_q:
                        sys.exit()
            bg_img = pygame.image.load('data/img/mw.jpg')
            bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
            screen.blit(bg_img, (0, 0))
            menu2.draw()
            pygame.display.flip()
    starttime = timeit.default_timer()
    bg_img = pygame.image.load('data/img/mw.jpg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    screen.blit(bg_img, (0, 0))
    menu = Menu(screen, 1)
    menu.draw()
    while in_game:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.KEYDOWN:
                if event.mod and pygame.K_q:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # todo 1: mouse release functionality with cell depressed
                location = pygame.mouse.get_pos()
                mo = menu.clicked(pygame.mouse.get_pos())
                if mo == 'Back':
                    in_game = False
                if mo == "X":
                    sys.exit()
                if (pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[2]) or pygame.mouse.get_pressed()[1]:
                    if board.middle_clicked(location):
                        in_game = False
                        after_game = True
                elif pygame.mouse.get_pressed()[0]:
                    if board.right_click(location):
                        in_game = False
                        after_game = True
                elif pygame.mouse.get_pressed()[2]:
                    board.left_click(location)
                # menu.draw()
        text = str(round(timeit.default_timer() - starttime, 1))
        text = font.render(text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width / 2, 50))
        r = pygame.Rect(screen_width/2, 50, 300, 200)
        r.center = (screen_width/2, 50)
        pygame.draw.rect(screen, (100, 100, 100), r, 0)
        pygame.draw.rect(screen, (0, 0, 0), r, 7)
        screen.blit(text, text_rect)


        match mode:
            case 'Beginner':
                if len(data[1]) > 5:
                    text = format(min([float(i) for i in data[1].replace('\n', '')[3:].split(',')]), '.2f')
                    text = font.render(text, True, (255, 0, 0))
                    text_rect = text.get_rect(center=(screen_width / 2, 100))
                    screen.blit(text, text_rect)
                else:
                    text = '-'
            case 'Custom':
                if len(data[0]) > 5:
                    text = format(min([float(i) for i in data[0].replace('\n', '')[3:].split(',')]), '.2f')
                    text = font.render(text, True, (255, 0, 0))
                    text_rect = text.get_rect(center=(screen_width / 2, 100))
                    screen.blit(text, text_rect)
                else:
                    text = '-'
            case 'Intermediate':
                if len(data[2]) > 5:
                    text = format(min([float(i) for i in data[2].replace('\n', '')[3:].split(',')]), '.2f')
                    text = font.render(text, True, (255, 0, 0))
                    text_rect = text.get_rect(center=(screen_width / 2, 100))
                    screen.blit(text, text_rect)
                else:
                    text = '-'
            case 'Advanced':
                if len(data[3]) > 5:
                    text = format(min([float(i) for i in data[3].replace('\n', '')[3:].split(',')]), '.2f')
                    text = font.render(text, True, (255, 0, 0))
                    text_rect = text.get_rect(center=(screen_width / 2, 100))
                    screen.blit(text, text_rect)
                else:
                    text = '-'
            case other:
                text = ''


        if board.draw():
            end = round(timeit.default_timer() - starttime, 2)
            # Won Game
            won = True
            in_game = False
            after_game = True
            match mode:
                case 'Beginner':
                    if len(data[1]) > 3:
                        if min([float(i) for i in data[1].replace('\n', '')[3:].split(',')]) > end:
                            record = True
                        data[1] = (data[1] + ', ' + str(end)).replace('\n', '') + '\n'
                    else:
                        first_game = True
                        data[1] = (data[1] + ' ' + str(end)).replace('\n', '') + '\n'
                case 'Intermediate':
                    if len(data[2]) > 3:
                        if min([float(i) for i in data[2].replace('\n', '')[3:].split(',')]) > end:
                            record = True
                        data[2] = (data[2] + ', ' + str(end)).replace('\n', '') + '\n'
                    else:
                        first_game = True
                        data[2] = (data[2] + ' ' + str(end)).replace('\n', '') + '\n'
                case 'Advanced':
                    if len(data[3]) > 3:
                        if min([float(i) for i in data[3].replace('\n', '')[3:].split(',')]) > end:
                            record = True
                        data[3] = (data[3] + ', ' + str(end)).replace('\n', '') + '\n'
                    else:
                        first_game = True
                        data[3] = (data[3] + ' ' + str(end)).replace('\n', '') + '\n'
                case 'Custom':
                    if len(data[0]) > 3:
                        if min([float(i) for i in data[0].replace('\n', '')[3:].split(',')]) > end:
                            record = True
                        data[0] = (data[0] + ', ' + str(end)).replace('\n', '') + '\n'
                    else:
                        first_game = True
                        data[0] = (data[0] + ' ' + str(end)).replace('\n', '') + '\n'

            with open('data/record.txt', 'w') as file:
                file.writelines(data)

        pygame.display.flip()
    if board is not False:
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
        font2 = pygame.font.SysFont('chalkduster.ttf', 200)
        if first_game:
            text = 'NICE!!!'
            text = font2.render(text, True, (10, 200, 10))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            text = str(end)
            text = font2.render(text, True, (10, 200, 10))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + 200))
            screen.blit(text, text_rect)

        elif record:
            text = 'RECORD!!!'
            text = font2.render(text, True, (10, 200, 10))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            text = str(end)
            text = font2.render(text, True, (10, 200, 10))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + 200))
            screen.blit(text, text_rect)
        elif won:
            text = 'Well Done!!'
            text = font2.render(text, True, (100, 100, 100))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            text = str(end)
            text = font2.render(text, True, (100, 100, 100))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + 200))
            screen.blit(text, text_rect)
        else:
            text = 'Try Again!!'
            text = font2.render(text, True, (100, 100, 100))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        after_game = False

if __name__ == '__main__':
    while(1):
        main()

