# Conway's Game of Life

Console utility for demonstrating the famous _"Conway's Game of Life"_. The implementation is made using the __Python__ language and _OOP_ principles.

## Information

The _Game of Life_, also known simply as _Life_, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the _Game of Life_ by creating an initial configuration and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing machine. 

<img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Conways_game_of_life_breeder_animation.gif">

Information taken from:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

### Rules

The universe of the _Game of Life_ is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These rules, which compare the behavior of the automaton to real life, can be condensed into the following:

- Any live cell with two or three live neighbours survives.
- Any dead cell with three live neighbours becomes a live cell.
- All other live cells die in the next generation. Similarly, all other dead cells stay dead.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.

Information taken from:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules

## Guide

### Settings

At the beginning of `main.py` file, there are a number of parameters that are set by default as:

```
MAX_X, MAX_Y = 50, 20
EMPTY, ALIVE = '.', 'x'
BORDER_CONJ = False
STEPS = 100
DELAY = 0.1
PROBABILITY = 0.3
SCREEN_HISTORY = False
```
Consider these parameters in more detail.

- `MAX_X, MAX_Y` &ndash; The dimensions of the space where the game takes place.
- `EMPTY` &ndash; The symbol that displays the "dead" cell. You can, for example, change it to a space (` `) to make the image visually less saturated.
- `ALIVE` &ndash; The symbol that displays the "live" cell. You can change it to any other character. But you need to remember that the examples of initial space configurations in additional files (`glider.txt`, `gun.txt`, `pulsar.txt`) use the `x` character and they will stop loading correctly.
- `BORDER_CONJ` &ndash; When the parameter is set to `True`, the boundaries of the space are conjugate: the top is connected to the bottom, and the left side is connected to the right.
- `STEPS` &ndash; Number of steps that the game continues. After the execution, you can set a new number of steps for the resulting configuration or exit the game.
- `DELAY` &ndash; The delay time between steps, in seconds. The larger it is, the slower the processes in the game.
- `PROBABILITY` &ndash; Number in the range from 0 to 1. Used to create a random initial configuration of the game. The smaller the number, the less populated the space is.
- `SCREEN_HISTORY` &ndash; To draw the game process, use the console screen. If this parameter is set to `True`, the screen will be cleared at each new step of the game. Otherwise, each next step will draw after the previous one. This will allow you to scroll through the steps after completing the game.

### Launch

To start the game with a randomly set initial configuration of cells, just run:
```
$ python main.py
```

In addition, you can load already set configurations from files. For example, a simple "spaceship" called a "glider" can be launched by a command:
```
$ python main.py glider.txt
```
<img src="https://upload.wikimedia.org/wikipedia/commons/f/f2/Game_of_life_animated_glider.gif">

An example of a periodic configuration ("oscillator") is a "pulsar".
```
$ python main.py pulsar.txt
```
<img src="https://upload.wikimedia.org/wikipedia/commons/0/07/Game_of_life_pulsar.gif">

An example of an infinitely growing configuration is the "Gosper's glider gun".
```
$ python main.py gun.txt
```
<img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif">

By analogy, you can create your own initial configuration of cells and check how it will develop in the game.