import pygame

from .cell import Cell
from random import randint


class Board:
    def __init__(self, cols: int, rows: int, bombs: int, screen: pygame.Surface):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.board = list()
        self.bombs = bombs
        self.cell_size = 30
        self.dx = self.screen.get_size()[0] / 2 - self.cell_size * self.cols / 2
        self.dy = self.screen.get_size()[1] / 2 - self.cell_size * self.rows / 2
        for i in range(cols):
            for j in range(rows):
                self.board.append(Cell(i, j, self.cols))
        self.bomb_positions = []
        while len(self.bomb_positions) < bombs:
            pos = (randint(0, cols - 1), randint(0, rows - 1))
            if pos not in self.bomb_positions:
                self.bomb_positions.append(pos)
        for locations in self.bomb_positions:
            self.board[locations[0] + cols * locations[1]].bomb = True

    def calculate(self):
        for cell in self.board:
            if cell.bomb is False:
                number = 0
                neighbours = cell.neighbours()
                for k in self.board:
                    if (k.location['x'], k.location['y']) in neighbours:
                        if k.bomb:
                            number += 1
                cell.number = number

    def debug(self):
        count = 1
        s = ''
        for i in self.board:
            if i.bomb:
                s += 'B'
            else:
                s += str(i.number)
            if count % self.cols == 0:
                print(s)
                s = ''
                count = 0
            count += 1

    def draw(self):
        revealed = 0
        for cell in self.board:
            if cell.revealed:
                revealed += 1
            if cell.revealed and cell.bomb:
                revealed = 10000000
            cell.draw(self.dx, self.dy, self.screen)
        if self.cols*self.rows - revealed == self.bombs:
            return True

    def middle_clicked(self, location: tuple):
        x = int((location[0] - self.dx) / self.cell_size)
        y = int((location[1] - self.dy) / self.cell_size)
        for cell in self.board:
            if cell.clicked((x, y)):
                if not cell.flagged:
                    if cell.revealed:
                        if self.chord(cell):
                            return True

    def right_click(self, location: tuple):
        x = int((location[0] - self.dx) / self.cell_size)
        y = int((location[1] - self.dy) / self.cell_size)
        for cell in self.board:
            if cell.clicked((x, y)):
                if not cell.flagged:
                    cell.revealed = True
                    if cell.number == 0:
                        self.scatter(cell, [])
                    elif cell.bomb:
                        return True
                return False

    def scatter(self, cell: Cell, seen_array):
        seen = seen_array
        seen.append(cell)
        n = cell.neighbours()
        for k in self.board:
            if (k.location['x'], k.location['y']) in n:
                if k.number == 0 and k.revealed is False and k not in seen:
                    k.revealed = True
                    self.scatter(k, seen)
                elif k.bomb is False and k not in seen:
                    k.revealed = True

    def chord(self, cell: Cell):
        n = cell.neighbours()
        flagged = 0
        n_temp = []
        for k in self.board:
            if (k.location['x'], k.location['y']) in n:
                if k.flagged:
                    flagged += 1
                else:
                    n_temp.append(k)
        if flagged == cell.number:
            for k in n_temp:
                k.revealed = True
                if k.number ==0:
                    self.scatter(k, [])
                if k.bomb:
                    return True


    def left_click(self, location: tuple):
        x = int((location[0] - self.dx) / self.cell_size)
        y = int((location[1] - self.dy) / self.cell_size)
        for cell in self.board:
            if cell.clicked((x, y)):
                if cell.revealed:
                    cell.flagged = False
                else:
                    cell.flagged = not cell.flagged
                break

    def reset(self):
        for cell in self.board:
            cell.revealed = True
            if cell.bomb:
                cell.number = -2
