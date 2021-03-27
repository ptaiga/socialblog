import os
import sys
from random import random as rand
from time import sleep

MAX_X, MAX_Y = 50, 20
EMPTY, ALIVE = '.', 'x'
BORDER_CONJ = False
STEPS = 10
DELAY = 0.1
PROBABILITY = 0.3
SCREEN_HISTORY = False


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False
        self.neighbors = []
        self.step = None

    def __repr__(self):
        return ALIVE if self.alive else EMPTY

    def set_rand(self, prob):
        self.alive = rand() < prob

    @property
    def num_alive_neigbors(self):
        return sum([n.alive for n in self.neighbors])

    def next_step(self):
        if not self.alive and self.num_alive_neigbors == 3:
            self.step = True
        elif self.alive and not self.num_alive_neigbors in [2, 3]:
            self.step = False
        else:
            self.step = self.alive

    def activate(self):
        self.alive = self.step


class Playground:

    def __init__(self, max_x, max_y, filename=None):
        self.max_x, self.max_y = max_x, max_y
        self.space = self.set_space(filename)
        self.set_neighbors()

    def set_space(self, filename):
        if filename:
            with open(filename, 'r') as f:
                file_data = f.read().splitlines()

            file_max_x = max([len(x) for x in file_data])
            file_max_y = len(file_data)
            self.max_x = max(file_max_x, self.max_x)
            self.max_y = max(file_max_y, self.max_y)

            space = [[Cell(x, y) for x in range(self.max_x)] 
                        for y in range(self.max_y)]

            for j, row in enumerate(file_data):
                for i, elem in enumerate(row):
                    if elem == ALIVE:
                        space[j][i].alive = True
        else:
            space = [[Cell(x, y) for x in range(self.max_x)] 
                        for y in range(self.max_y)]
            for j in range(self.max_y):
                for i in range(self.max_x):
                    space[j][i].set_rand(PROBABILITY)
        return space

    def set_neighbors(self):
        for j in range(self.max_y):
            for i in range(self.max_x):
                if BORDER_CONJ:
                    up = (j + 1) if j < (self.max_y - 1) else 0
                    right = (i + 1) if i < (self.max_x - 1) else 0
                    self.space[j][i].neighbors = [
                        self.space[j-1][i], self.space[j][i-1],
                        self.space[up][i], self.space[j][right],
                        self.space[j-1][i-1], self.space[up][right],
                        self.space[j-1][right], self.space[up][i-1],
                    ]
                else:
                    self.space[j][i].neighbors = []
                    if j == 0:
                        if i == 0: 
                            self.space[j][i].neighbors += [
                                self.space[j+1][i],
                                self.space[j][i+1],
                                self.space[j+1][i+1],
                            ]
                        elif i == (self.max_x - 1):
                            self.space[j][i].neighbors += [
                                self.space[j+1][i],
                                self.space[j][i-1],
                                self.space[j+1][i-1],
                            ]
                        else:
                            self.space[j][i].neighbors += [
                                self.space[j+1][i],
                                self.space[j][i+1], self.space[j][i-1],
                                self.space[j+1][i+1], self.space[j+1][i-1],
                            ]
                    elif j == (self.max_y - 1):
                        if i == 0: 
                            self.space[j][i].neighbors += [
                                self.space[j-1][i],
                                self.space[j][i+1],
                                self.space[j-1][i+1],
                            ]
                        elif i == (self.max_x - 1):
                            self.space[j][i].neighbors += [
                                self.space[j-1][i],
                                self.space[j][i-1],
                                self.space[j-1][i-1],
                            ]
                        else:
                            self.space[j][i].neighbors += [
                                self.space[j-1][i],
                                self.space[j][i+1], self.space[j][i-1],
                                self.space[j-1][i+1], self.space[j-1][i-1],
                            ]
                    else:
                        if i == 0: 
                            self.space[j][i].neighbors += [
                                self.space[j+1][i], self.space[j-1][i],
                                self.space[j][i+1],
                                self.space[j+1][i+1], self.space[j-1][i+1],
                            ]
                        elif i == (self.max_x - 1):
                            self.space[j][i].neighbors += [
                                self.space[j+1][i], self.space[j-1][i],
                                self.space[j][i-1],
                                self.space[j+1][i-1], self.space[j-1][i-1],
                            ]
                        else:
                            self.space[j][i].neighbors += [
                                self.space[j+1][i], self.space[j-1][i],
                                self.space[j][i+1], self.space[j][i-1],
                                self.space[j+1][i+1], self.space[j-1][i+1],
                                self.space[j+1][i-1], self.space[j-1][i-1],
                            ]

    def draw(self):
        if not SCREEN_HISTORY:
            os.system('clear||cls')
        for j in range(self.max_y):
            for i in range(self.max_x):
                print(self.space[j][i], end="")
            print("")

    def play(self):
        [[cell.next_step() for cell in row] for row in self.space]
        [[cell.activate() for cell in row] for row in self.space]


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    pg = Playground(MAX_X, MAX_Y, filename)
    pg.draw()
    play = True
    itterations = 0
    steps = STEPS
    while(play):
        play = False
        for i in range(steps):
            pg.play()
            if SCREEN_HISTORY:
                print('-' * (pg.max_x + 1))
            pg.draw()
            sleep(DELAY)
        itterations += steps
        print(f"Performed {itterations} steps.")
        res = input("Enter number of next steps: ")
        if res.isdigit():
            steps = int(res)
            play = True


if __name__ == "__main__":
    main()