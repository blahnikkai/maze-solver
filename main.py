from maze import Maze, Coord, generate_empty_square_maze
from graphics import Board
from generation import GeneratedMaze


def test_search():
    spaces = generate_empty_square_maze(100)
    start = Coord(1, 1)
    end = Coord(0, 0)
    maze = Maze(spaces, start, end)

    gen = GeneratedMaze(9)

    gen.dfs()


def test_graphics():
    spaces = [
        [1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0]
    ]
    start = Coord(1, 1)
    end = Coord(4, 5)
    maze = Maze(spaces, start, end)

    maze.randomize(20, .3)
    board = Board(maze)

    board.show_callback(maze.bfs, None)


def test_generation():
    gen = GeneratedMaze()
    gen.generate()
    board = Board(gen)
    board.root.mainloop()


def main():
    test_generation()


if __name__ == '__main__':
    main()
