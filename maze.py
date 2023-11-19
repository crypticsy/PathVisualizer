import numpy as np
from tabulate import tabulate


class Tile:
    def __init__(self, y, x):
        # Initialize a tile with coordinates (y, x)
        self.x = x
        self.y = y
        
        # By default, the tile is not an obstacle, start or goal
        self.obstacle = False
        self.is_start = False
        self.is_goal = False
        self.is_visited = False
    
    def get_coordinates(self):
        # Return the coordinates of the tile
        return (self.x, self.y)

    def set_obstacle(self):
        # Set the tile as an obstacle
        self.obstacle = True
    
    def set_visited(self):
        # Set the tile as visited
        self.is_visited = True

    def set_start(self):
        # Set the tile as the start tile
        self.is_start = True

    def set_goal(self):
        # Set the tile as the goal tile
        self.is_goal = True

    def is_obstacle(self):
        # Check if the tile is an obstacle
        return self.obstacle

    def __str__(self):
        # Print the coordinates of the tile
        if self.is_start: return "S"
        elif self.is_goal: return "G"
        elif self.is_obstacle(): return "#"
        elif self.is_visited: return "O"
        return "."
    
    def __repr__(self):
        # String representation of the tile for debugging
        return f"Tile({self.x}, {self.y}, obstacle={self.obstacle}, start={self.is_start}, goal={self.is_goal})"
    
    def __lt__(self, other):
        # Compare tiles based on their coordinates
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __gt__(self, other):
        # Compare tiles based on their coordinates
        if self.x == other.x:
            return self.y > other.y
        return self.x > other.x

    def __hash__(self):
        # Hash the tile based on its coordinates
        return hash((self.x, self.y))



class Maze:
    def __init__(self, width, height):
        # Initialize the maze with the given width and height
        self.width = width
        self.height = height
        # Create a grid of tiles using NumPy array
        self.grid = np.array([[Tile(y, x) for y in range(height)] for x in range(width)])
        
        # Initialize start and goal positions (set to None initially)
        self.start_pos = None
        self.goal_pos = None
    
    def __str__(self):
        # Print the maze
        return tabulate(self.grid, tablefmt="fancy_grid", stralign="center")

    def set_obstacle(self, y, x):
        # Set the tile at coordinates (y, x) as an obstacle
        self.grid[y, x].set_obstacle()
    
    def set_visited(self, y, x):
        # Set the tile at coordinates (y, x) as visited
        self.grid[y, x].set_visited()
    
    def clear_visited(self):
        # Clear all visited tiles
        for row in self.grid:
            for tile in row:
                tile.is_visited = False

    def is_obstacle(self, y, x):
        # Check if the tile at coordinates (y, x) is an obstacle
        return self.grid[y, x].is_obstacle()

    def set_start(self, y, x):
        # Set the start position
        self.start_pos = (y, x)
        self.grid[y, x].set_start()

    def set_goal(self, y, x):
        # Set the goal position
        self.goal_pos = (y, x)
        self.grid[y, x].set_goal()

    def get_neighbors(self, y, x):
        # Get neighboring coordinates that can be reached from (y, x)
        neighbors = []

        # Check if there is a tile to the left and it is not an obstacle
        if y > 0 and not self.is_obstacle(y - 1, x):
            neighbors.append((y - 1, x))

        # Check if there is a tile to the right and it is not an obstacle
        if y < self.width - 1 and not self.is_obstacle(y + 1, x):
            neighbors.append((y + 1, x))

        # Check if there is a tile above and it is not an obstacle
        if x > 0 and not self.is_obstacle(y, x - 1):
            neighbors.append((y, x - 1))

        # Check if there is a tile below and it is not an obstacle
        if x < self.height - 1 and not self.is_obstacle(y, x + 1):
            neighbors.append((y, x + 1))

        return neighbors