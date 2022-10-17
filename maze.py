from collections import deque
from dataclasses import dataclass
from random import random, randint
from time import sleep


# from graphics import Board


@dataclass(eq=True, frozen=True)
class Coord:
    r: int
    c: int


def generate_empty_square_maze(n: int) -> [int]:
    spaces = []
    for r in range(n):
        spaces.append([])
        for c in range(n):
            spaces[r].append(0)
    return spaces


def get_adjacent(c: Coord) -> list[Coord]:
    up = Coord(c.r - 1, c.c)
    right = Coord(c.r, c.c + 1)
    down = Coord(c.r + 1, c.c)
    left = Coord(c.r, c.c - 1)
    return [up, right, down, left]


def update_board(board, delay: float, coords: [Coord]) -> None:
    if board:
        board.update(coords)
        board.root.update()
        sleep(delay)


class Maze:

    def __str__(self) -> str:
        text = '   '
        for c in range(self.size):
            text += f'{c}  '
        text += '\n'
        for r, row in enumerate(self.spaces):
            for c, space in enumerate(row):
                if c == 0:
                    text += f'{r}  '
                coord = Coord(r, c)
                if coord == self.start:
                    text += 'p  '
                    continue
                if coord == self.end:
                    text += 'e  '
                    continue
                if coord in self.visited:
                    text += 'v  '
                    continue
                conversion = {0: '.',
                              1: '■'}
                text += str(conversion[space])
                text += '  '
            text += '\n'
        return text

    def __init__(self, spaces: list[list[int]], start: Coord, end: Coord = None):
        if spaces is None:
            return
        self.spaces = spaces
        self.size = len(spaces)
        self.start = start
        self.end = end
        self.visited = set()
        self.found = set()
        assert len(spaces) == len(spaces[0]), 'Maze must be square'
        assert end is None or start != end, 'Entrance and exit cannot be the same space'

        assert spaces[start.r][start.c] != 1, 'Entrance must not be on a wall'
        assert end is None or spaces[end.r][end.c] != 1, 'Exit must not be on a wall'

    def randomize(self, n: int, p: float) -> None:
        self.reset()
        self.size = n
        self.size = n
        self.spaces = []
        for r in range(n):
            self.spaces.append([])
            for c in range(n):
                space = 0
                if random() < p:
                    space = 1
                self.spaces[r].append(space)
        en = Coord(-1, -1)
        while not self.check_movable(en):
            en = Coord(randint(0, self.size), randint(0, self.size))
        self.start = en
        ex = Coord(-1, -1)
        while not self.check_movable(ex):
            ex = Coord(randint(0, self.size), randint(0, self.size))
        self.end = ex

    def reset(self) -> None:
        self.visited = set()
        self.found = set()

    def random_movable_coord(self) -> Coord:
        coord = Coord(-1, -1)
        while not self.check_movable(coord):
            coord = Coord(randint(0, self.size), randint(0, self.size))
        return coord

    def check_movable(self, coord: Coord) -> bool:
        r = coord.r
        c = coord.c
        return 0 <= r < self.size and 0 <= c < self.size \
               and not self.spaces[r][c] and coord not in self.visited

    def dfs(self, board=None, delay: float = 0) -> [Coord]:
        return self.simple_search(board, delay, False)

    def bfs(self, board=None, delay: float = 0) -> [Coord]:
        return self.simple_search(board, delay, True)

    def simple_search(self, board, delay: float, mode: bool) -> [Coord]:
        paths = deque([[self.start]])
        while paths:
            if mode:
                path = paths.popleft()
            else:
                path = paths.pop()
            curr = path[-1]
            if curr == self.end:
                self.found = set(path)
                update_board(board, 0, path)
                return path
            if not self.check_movable(curr):
                continue
            self.visited.add(curr)
            update_board(board, delay, [curr])

            adjacents = get_adjacent(curr) if mode else reversed(get_adjacent(curr))
            for adjacent in adjacents:
                if self.check_movable(adjacent):
                    paths.append(path + [adjacent])
        return None

    # recursively solves maze
    def dfs_recursive(self, p: Coord) -> bool:
        self.visited.add(p)
        print(self)
        if p == self.end:
            print(f'Found at row {p.r} column {p.c}')
            return True
        for adjacent in get_adjacent(p):
            if self.check_movable(adjacent):
                if self.dfs_recursive(adjacent):
                    return True
        return False
