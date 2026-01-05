import random
from typing import NamedTuple
from tabulate import tabulate
from IPython.core.display import HTML


class Coordinate(NamedTuple):
    """Maze locations in the grid as x, y coordinates"""
    x: int
    y: int


class MazeSymbol:
    """Symbols to use when printing the maze"""
    start_node = "S"
    end_node = "E"
    wall = "X"
    empty = " "
    path = "*"


default_obstacles = set()

class Maze:

    def __init__(
        self,
        rows=30,
        columns=30,
        barriers=0.2,
        start_node=None,
        end_node=None,
        random_obstacles=False,
        custom_obstacles=default_obstacles):

            # Maze Dimensions
            self.rows = rows
            self.columns = columns

            # Density of Barriers (Obstacles)
            self.barriers = barriers

            # Start and End Nodes (dynamic based on grid size)
            self.start_node = start_node if start_node is not None else Coordinate(0, 0)
            self.end_node = end_node if end_node is not None else Coordinate(rows - 1, columns - 1)
            
            # Obstacle Configuration
            self.custom_obstacles = custom_obstacles
            self.random_obstacles = random_obstacles
                
            # Maze Initialization
            self.maze = [[MazeSymbol.empty for col in range(columns)] for row in range(rows)]
            
            # Fill Maze with Obstacles
            self._fill_maze(self.random_obstacles)

    def _fill_maze(self, random_obstacles):
        """ Fills the maze with obstacles based on the specified configuration."""

        # Loop through each cell in the maze
        for row in range(self.rows):
            for col in range(self.columns):
                # If random obstacles are enabled and a random value is within the barrier density
                if random_obstacles and random.uniform(0, 1) <= self.barriers:
                    self.maze[row][col] = MazeSymbol.wall
                # If custom obstacles are specified and the current cell is in the custom obstacles list
                elif not random_obstacles and (row, col) in self.custom_obstacles:
                    self.maze[row][col] = MazeSymbol.wall

        # Set the start and end nodes in the maze
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
    
    def draw_weighted_path(self, path, weights):
        for loc in path:
            self.maze[loc.x][loc.y] = weights[loc]

    def clear_path(self, path):
        for loc in path:
            self.maze[loc.x][loc.y] = MazeSymbol.empty

    def __str__(self):
        """Prints the current maze state if used outside of browser, mainly for debugging"""
        return tabulate(self.maze, tablefmt="heavy_grid", stralign="center")
    
    def copy(self):
        """Returns a copy of the current maze"""
        return Maze(
            rows=self.rows,
            columns=self.columns,
            barriers=self.barriers,
            start_node=self.start_node,
            end_node=self.end_node,
            random_obstacles=self.random_obstacles,
            custom_obstacles=self.custom_obstacles
        )
    
    def display_maze(self, return_html=False):
        """Draws the maze in the browser"""

        html_content = ""
        cell_type = {
            'S' : 'bg-green-700',
            ' ' : 'bg-white/20',
            'E' : 'bg-red-700',
            'X' : 'bg-slate-800',
        }

        for row in self.maze:
            html_content += "<div class='flex flex-row'>"
            for node in row:
                current_class = "bg-slate-500/50" if node not in cell_type else cell_type[node]
                html_content += f"<div class='flex flex-col w-12 h-12 text-center justify-center font-bold border-2 border-gray-200/20 {current_class} '>{node}</div>"
            html_content += "</div>"


        html_content = f"""
        <table class="table-auto">
            {html_content}
        </table>
        """

        if return_html: return html_content
        return HTML(html_content)

    @classmethod
    def from_grid_state(cls, grid_state, start, end):
        """
        Create a Maze from a client-provided grid state.

        Args:
            grid_state: 2D list where True = wall, False = empty
            start: [row, col] of start position
            end: [row, col] of end position

        Returns:
            Maze instance
        """
        rows = len(grid_state)
        cols = len(grid_state[0]) if rows > 0 else 0

        # Find all wall positions
        obstacles = set()
        for r in range(rows):
            for c in range(cols):
                if grid_state[r][c]:
                    obstacles.add((r, c))

        return cls(
            rows=rows,
            columns=cols,
            start_node=Coordinate(start[0], start[1]),
            end_node=Coordinate(end[0], end[1]),
            random_obstacles=False,
            custom_obstacles=obstacles
        )


def draw_mazes(mazes, title, final_path_lenth, runtime, final_maze):
        output = ""
        for n, maze in enumerate(mazes):
            output += f"""
                <div class="flex flex-col justify-center items-center space-y-4 p-4">
                    <div class="flex flex-col justify-center items-center">
                        <div class="text-lg font-bold text-center">State: {n}</div>
                    </div>
                    <div class="flex flex-col">
                        {maze}
                    </div>
                </div>
            """
        
        output += f"""
            <div class="flex flex-col justify-center items-center space-y-4 p-4 bg-gradient-to-r from-green-300/50 to-green-800/50">
                <div class="flex flex-col justify-center items-center">
                    <div class="text-lg font-bold text-center">Final Path</div>
                </div>
                <div class="flex flex-col">
                    {final_maze}
                </div>
            </div>
        """
        
        
        output = f"""
            <div class="flex flex-col justify-center items-center py-8">
                <div class="text-2xl font-bold text-center pb-3">{title}</div>
                <div class="flex flex-row justify-center items-center space-x-8">
                    <div class="text-lg text-center">Nodes Explored: {len(mazes)}</div>
                    <div class="text-lg text-center">Final Path Length: {final_path_lenth}</div>
                    <div class="text-lg text-center">Runtime: {runtime}</div>
                </div>
            </div>
            <div class="grid grid-cols-5 justify-center items-center">
                {output}
            </div>
        """
        
        return HTML(output)