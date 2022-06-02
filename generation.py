from collections import deque
from random import shuffle
from maze import Maze, Coord, update_board


def get_generation_adjacent(c: Coord) -> list[tuple[Coord, Coord]]:
    ups = (Coord(c.r - 1, c.c), Coord(c.r - 2, c.c))
    rights = (Coord(c.r, c.c + 1), Coord(c.r, c.c + 2))
    downs = (Coord(c.r + 1, c.c), Coord(c.r + 2, c.c))
    lefts = (Coord(c.r, c.c - 1), Coord(c.r, c.c - 2))
    return [ups, rights, downs, lefts]


class GeneratedMaze(Maze):

    def __init__(self, n: int = 25):
        assert n % 2 == 1, 'The size of the maze must be odd'
        spaces = []
        for r in range(n):
            spaces.append([])
            for c in range(n):
                if r % 2 == 1 and c % 2 == 1:
                    spaces[r].append(0)
                else:
                    spaces[r].append(1)
        super().__init__(spaces, Coord(1, 1))

    def generate(self, board=None, delay: float = 0) -> None:
        connected = set()
        q = deque([(self.start, self.start)])
        while q:
            wall, curr = q.pop()
            if not self.check_movable(curr) or curr in connected:
                continue
            if wall:
                self.spaces[wall.r][wall.c] = 0
            connected.add(curr)
            update_board(board, delay, [wall])

            adjacents = get_generation_adjacent(curr)
            shuffle(adjacents)
            for adjacent in adjacents:
                if self.check_movable(adjacent[1]):
                    q.append(adjacent)

        self.end = self.random_movable_coord()
        update_board(board, 0, [self.end])


