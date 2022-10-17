from generation import GeneratedMaze
from maze import Maze, Coord
from tkinter import Frame, Tk, Radiobutton, IntVar, Button

VIEW_SIZE = 600
WIDTH = 8
PAD = 10


def set_all_buttons(buttons, state: str) -> None:
    for button in buttons:
        button.config(state=state)


class Board:

    def __init__(self, maze: Maze):
        self.root = Tk()
        self.root.title('Maze Machine')
        self.root.resizable(False, False)

        self.quit = False
        self.in_process = False
        self.selection = 0

        # self.root.bind('<KeyPress>', self.on_key_press)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.maze = maze
        self.tiles = []
        self.init_center()

        self.init_controls()

    def init_center(self) -> None:
        center = Frame(self.root, bg='black', width=VIEW_SIZE, height=VIEW_SIZE)
        center.grid(row=0, column=1)
        for r in range(self.maze.size):
            self.tiles.append([])
            for c in range(self.maze.size):
                tile = Frame(center, width=VIEW_SIZE / self.maze.size, height=VIEW_SIZE / self.maze.size)
                tile.grid(row=r, column=c)
                tile.bind('<1>', lambda event, coord=Coord(r, c): self.on_mouse_click(event, coord))
                self.tiles[r].append(tile)
                self.__update_tile(Coord(r, c))

    def init_controls(self) -> None:
        controls = Frame(self.root, bg='black', width=200, height=VIEW_SIZE, pady=100)
        controls.grid(row=0, column=0)
        controls.grid_propagate(False)

        controls.grid_columnconfigure(0, weight=1)

        choices = {
            'Start': 0,
            'End': 1
        }
        row = iter(range(10))

        radios = []
        var = IntVar(value=2)
        for text, value in choices.items():
            radio = Radiobutton(controls, text=text, value=value, bg='black', fg='white', variable=var,
                                command=lambda: self.select(var), activebackground='blue')
            radio.grid(row=next(row), column=0)
            radios.append(radio)

        bfs_button = Button(controls, width=WIDTH, text='BFS')
        bfs_button.grid(row=next(row), column=0, pady=PAD)
        dfs_button = Button(controls, width=WIDTH, text='DFS')
        dfs_button.grid(row=next(row), column=0, pady=PAD)
        regenerate_button = Button(controls, width=WIDTH, text='Generate\nNew Maze')
        regenerate_button.grid(row=next(row), column=0, pady=PAD)

        all_buttons = [bfs_button, dfs_button, regenerate_button, *radios]

        bfs_button.config(command=lambda: self.show_callback(self.maze.bfs, radios))
        dfs_button.config(command=lambda: self.show_callback(self.maze.dfs, radios))
        regenerate_button.config(command=lambda: self.regenerate(all_buttons))

    def reset(self) -> None:
        self.maze.reset()
        self.update_all()

    def regenerate(self, buttons) -> None:
        self.maze = GeneratedMaze()
        self.show_callback(self.maze.generate, buttons)

    def select(self, var) -> None:
        self.selection = var.get()

    def on_quit(self) -> None:
        self.quit = True
        quit(0)

    def show_callback(self, callback: callable, buttons: [Button]) -> None:
        self.in_process = True
        set_all_buttons(buttons, 'disabled')

        self.reset()
        delay = 31.25 / (self.maze.size ** 2)
        callback(self, delay)

        self.in_process = False
        set_all_buttons(buttons, 'normal')

    def update_all(self) -> None:
        for r, row in enumerate(self.maze.spaces):
            for c, space in enumerate(row):
                self.__update_tile(Coord(r, c))

    def update(self, coords: [Coord]):
        for coord in coords:
            if coord:
                self.__update_tile(coord)

    def __update_tile(self, coord: Coord) -> None:
        if self.quit:
            quit(1)

        r = coord.r
        c = coord.c
        space = self.maze.spaces[r][c]

        color = 'white'
        if space == 1:
            color = 'black'
        if coord in self.maze.visited:
            color = '#bbbbbb'
        if coord in self.maze.found:
            color = 'red'
        if coord == self.maze.start:
            color = 'orange'
        if coord == self.maze.end:
            color = 'green'

        self.tiles[r][c].configure(bg=color)

    def on_mouse_click(self, e, coord: Coord) -> None:
        if self.in_process:
            return
        if coord == self.maze.start:
            return
        r = coord.r
        c = coord.c
        to_update = [coord]

        curr_space = self.maze.spaces[r][c]
        if self.selection == 0 and not curr_space and coord != self.maze.end:
            # Do not reorder
            to_update.append(self.maze.start)
            self.maze.start = coord
        if self.selection == 1 and not curr_space:
            to_update.append(self.maze.end)
            if coord == self.maze.end:
                self.maze.end = None
            else:
                self.maze.end = coord
        self.update(to_update)

    # # w 119
    # # a 97
    # # s 115
    # # d 100
    # def on_key_press(self, e):
    #     old_p = self.maze.start
    #     [up, right, down, left] = get_adjacent(self.maze.start)
    #     if e.keycode == 119:
    #         if self.maze.check_movable(up):
    #             self.maze.start = up
    #     if e.keycode == 100:
    #         if self.maze.check_movable(right):
    #             self.maze.start = right
    #     if e.keycode == 115:
    #         if self.maze.check_movable(down):
    #             self.maze.start = down
    #     if e.keycode == 97:
    #         if self.maze.check_movable(left):
    #             self.maze.start = left
    #     self.update([old_p, self.maze.start])
