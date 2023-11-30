import random
from typing import NamedTuple


class Coordinate(NamedTuple):
    """Maze locations in the grid as x, y coordinates"""
    x: int
    y: int


class MazeSymbol:
    """Symbols to use when printing the maze"""
    start_node = "S"
    end_node = "F"
    wall = "X"
    empty = " "
    path = "*"


default_obstacles = set([
    (0, 1),
    (2, 1),
    (2, 3),
    (3, 1),
    (3, 4),
    (4, 4)
])


class Maze:
    def __init__(
        self, 
        rows=5, 
        columns=6, 
        barriers=0.2, 
        start_node=Coordinate(0, 0), 
        end_node=Coordinate(4, 5),
        random_obstacles=False):
        
            self.rows = rows
            self.columns = columns
            self.barriers = barriers
            self.start_node = start_node
            self.end_node = end_node
            self.maze = [[MazeSymbol.empty for col in range(columns)] for row in range(rows)]
            self._fill_maze(random_obstacles)

    def _fill_maze(self, random_obstacles):
        for row in range(self.rows):
            for col in range(self.columns):
                if random_obstacles and random.uniform(0, 1) <= self.barriers:
                    self.maze[row][col] = MazeSymbol.wall
                elif not random_obstacles and (row, col) in default_obstacles:
                    self.maze[row][col] = MazeSymbol.wall
                    
        self.maze[self.start_node.x][self.start_node.y] = MazeSymbol.start_node
        self.maze[self.end_node.x][self.end_node.y] = MazeSymbol.end_node

    def get_neighbors(self, curr):
        """curr is a Location for current location"""
        next_moves = []
        # Move one position up
        if curr.x - 1 >= 0 and self.maze[curr.x - 1][curr.y] != MazeSymbol.wall:
            next_moves.append(Coordinate(curr.x - 1, curr.y))
        # Move one position left
        if curr.y - 1 >= 0 and self.maze[curr.x][curr.y - 1] != MazeSymbol.wall:
            next_moves.append(Coordinate(curr.x, curr.y - 1))
        # Move one position right
        if curr.y + 1 < self.columns and self.maze[curr.x][curr.y + 1] != MazeSymbol.wall:
            next_moves.append(Coordinate(curr.x, curr.y + 1))
        # Move one position down
        if curr.x + 1 < self.rows and self.maze[curr.x + 1][curr.y] != MazeSymbol.wall:
            next_moves.append(Coordinate(curr.x + 1, curr.y))
        return next_moves

    def end_node_line(self, curr):
        if curr.x == self.end_node.x and curr.y == self.end_node.y:
            return True
        return False

    def draw_path(self, path):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.path

    def clear_path(self, path):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.empty

    def __str__(self):
        """Prints the current maze state if used outside of browser, mainly for debugging"""
        pretty_printed = ''
        for num, row in enumerate(self.maze):
            if num == 0:
                pretty_printed += "".join("_" for i in range(self.columns + 2)) + "\n"
            pretty_printed += "|"
            for space in row:
                pretty_printed += space
            if num == (self.columns - 1):
                pretty_printed += "|\n" + "".join("-" for i in range(self.columns + 2)) + "\n"
                break
            pretty_printed += "|\n"
        return pretty_printed
