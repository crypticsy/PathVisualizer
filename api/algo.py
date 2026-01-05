from math import sqrt
from collections import deque
from heapq import heappush, heappop
from api.maze import Coordinate, MazeSymbol

class Stack:
    def __init__(self):
        self._next_moves = []

    def push(self, loc):
        self._next_moves.append(loc)

    def pop(self):
        return self._next_moves.pop()

    @property
    def stuck(self):
        return not self._next_moves

    def __repr__(self):
        if self._next_moves:
            return repr([(loc.x, loc.y) for loc in self._next_moves])
        return None


class Queue:
    def __init__(self):
        self._next_moves = deque()

    def push(self, loc):
        self._next_moves.append(loc)

    def pop(self):
        return self._next_moves.popleft()

    @property
    def stuck(self):
        return not self._next_moves

    def __repr__(self):
        if self._next_moves:
            return repr([(loc.x, loc.y) for loc in self._next_moves])
        return None
    
class PriorityQueue:
    def __init__(self):
        self._container = []

    @property
    def empty(self):
        return not self._container

    def push(self, item):
        heappush(self._container, item)

    def pop(self):
        return heappop(self._container)

    def __repr__(self):
        return repr(self._container)


class Move:
    def __init__(self, current, previous, cost=0.0, heuristic=0.0):
        self.current = current
        self.previous = previous
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        """
        This method is a comparison of cost functions for two moves based on the heurist function to the maze end.
        :param other: another object of class Move
        :return: Bool
        """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def manhattan_distance(finish):
    # Simple Manhattan distance heuristic
    def distance(loc):
        return abs(loc.y - finish.y) + abs(loc.x - finish.x)
    return distance

def euclidean_distance(finish_line):
    # Simple Euclidean distance heuristic
    def distance(loc):
        xdistance = loc.column - finish_line.column
        ydistance = loc.row - finish_line.row
        return sqrt((xdistance ** 2) + (ydistance ** 2))
    return distance


def reconstruct_path(locations):
    # Initialize an empty list to store the reconstructed path
    path = []

    # Iterate through the locations, moving backward in the path
    while locations.previous is not None:
        locations = locations.previous
        path.append(locations.current)

    # Reverse the path to start from the beginning
    return path[::-1]


# Depth-First Search Algorithm
def depth_first_search(maze):
    # Initialize a stack for DFS
    stack = Stack()
    stack.push(Move(maze.start_node, None))
    
    # Track visited nodes to avoid loops
    visited_node = {maze.start_node}
    
    # List to store all explored paths
    all_paths = []
    
    # Main DFS loop
    while not stack.stuck:
        loc = stack.pop()
        active = loc.current
        all_paths.append(active)
        
        # Check if the end node is reached
        if maze.end_node_line(active):
            final_path = reconstruct_path(loc)
            return final_path[1:], all_paths[1:-1]
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(active):
            if neighbor not in visited_node:
                visited_node.add(neighbor)
                stack.push(Move(neighbor, loc))
    
    # Return None if no maze solution is found
    return None, None


# Breadth-First Search Algorithm
def breadth_first_search(maze):
    # Initialize a queue for BFS
    queue = Queue()
    queue.push(Move(maze.start_node, None))
    
    # Track visited nodes to avoid revisiting
    visited_node = {maze.start_node}
    
    # List to store all explored paths
    all_paths = []
    
    # Main BFS loop
    while not queue.stuck:
        loc = queue.pop()
        active = loc.current
        all_paths.append(active)
        
        # Check if the end node is reached
        if maze.end_node_line(active):
            final_path = reconstruct_path(loc)
            return final_path[1:], all_paths[1:-1]
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(active):
            if neighbor not in visited_node:
                visited_node.add(neighbor)
                queue.push(Move(neighbor, loc))
    
    # Return None if no maze solution is found
    return None, None


# A* Search Algorithm
def a_star(maze, heuristic_func, return_weights=False):
    # Initialize a priority queue for A*
    frontier = PriorityQueue()
    heuristic = heuristic_func(maze.end_node)
    frontier.push(Move(maze.start_node, None, 0.0, heuristic(maze.start_node)))
    
    # Track visited nodes and their costs
    visited_node = {maze.start_node: 0.0}
    
    # List to store all explored paths
    all_paths = []
    
    # Main A* loop
    while not frontier.empty:
        loc = frontier.pop()
        active = loc.current
        all_paths.append(active)
        
        # Check if the end node is reached
        if maze.end_node_line(active):
            final_path = reconstruct_path(loc)
            if return_weights: return final_path[1:], all_paths[1:-1], visited_node
            return final_path[1:], all_paths[1:-1]
        
        # Explore neighbors
        for neighbor in maze.get_neighbors(active):
            new_cost = loc.cost + 1
            
            # Update cost if a shorter path is found
            if neighbor not in visited_node or visited_node[neighbor] > new_cost:
                visited_node[neighbor] = new_cost
                frontier.push(Move(neighbor, loc, new_cost, heuristic(neighbor)))

    # Return None if no maze solution is found
    if return_weights: return None, None, visited_node
    return None, None


# Define a function to combine two dictionaries of weights
def combine_weights(weights1, weights2):
    # Create a copy of the first dictionary to avoid modifying the original
    combined_weights = {**weights1}
    
    # Iterate through the second dictionary
    for key, value in weights2.items():
        # Update the combined weights if the key is not present or if the new value is smaller
        if key not in combined_weights or combined_weights[key] > value:
            combined_weights[key] = value
    
    # Return the combined weights
    return combined_weights

# Define a function to get unique paths from a list of paths
def get_unique_paths(all_paths):
    # Initialize a list to store unique paths
    unique_paths = []
    
    # Iterate through all paths
    for path in all_paths:
        # Check if the path was already added
        if path not in unique_paths:
            unique_paths.append(path)

    # Return the unique paths
    return unique_paths


# Define the bidirectional heuristic search algorithm
def bidirectional_heuristic_search(maze, heuristic_func, return_weights=False):
    # Initialize a priority queue for A* from the start node
    frontier = PriorityQueue()
    heuristic1 = heuristic_func(maze.end_node)
    frontier.push(Move(maze.start_node, None, 0.0, heuristic1(maze.start_node)))
    
    # Initialize a priority queue for A* from the end node
    frontier2 = PriorityQueue()
    heuristic2 = heuristic_func(maze.start_node)
    frontier2.push(Move(maze.end_node, None, 0.0, heuristic2(maze.end_node)))
    
    # Track visited nodes and their costs for each direction
    visited_node = {maze.start_node: 0.0}
    visited_node2 = {maze.end_node: 0.0}
    
    # List to store all explored paths
    all_paths = []
    
    # Main bidirectional A* loop
    while not frontier.empty and not frontier2.empty:
        # Process A* from the start node
        loc = frontier.pop()
        active = loc.current
        all_paths.append(active)
        
        # Process A* from the end node
        loc2 = frontier2.pop()
        active2 = loc2.current
        all_paths.append(active2)
        
        # Check if the two paths meet
        if active in visited_node2 or active2 in visited_node:
            # Determine the meeting point and combine paths
            if active in visited_node2:
                mid_point = active
                while loc2:
                    if loc2.current in visited_node: break
                    loc2 = frontier2.pop()
            else:
                mid_point = active2
                while loc:
                    if loc.current in visited_node2: break
                    loc = frontier.pop()

            # Combine paths and reverse the path from the end to meeting point
            actual_final_path = get_unique_paths(reconstruct_path(loc)[1:] + [mid_point] + reconstruct_path(loc2)[1:][::-1])
            
            # Return the final path and additional information if requested
            if return_weights: return actual_final_path, get_unique_paths(all_paths[2:]), combine_weights(visited_node, visited_node2)
            return actual_final_path, get_unique_paths(all_paths[2:])
        
        # Explore neighbors for A* from the start node
        for neighbor in maze.get_neighbors(active):
            new_cost = loc.cost + 1
            
            # Update cost if a shorter path is found
            if neighbor not in visited_node or visited_node[neighbor] > new_cost:
                visited_node[neighbor] = new_cost
                frontier.push(Move(neighbor, loc, new_cost, heuristic1(neighbor)))
        
        # Explore neighbors for A* from the end node
        for neighbor in maze.get_neighbors(active2):
            new_cost = loc2.cost + 1
            
            # Update cost if a shorter path is found
            if neighbor not in visited_node2 or visited_node2[neighbor] > new_cost:
                visited_node2[neighbor] = new_cost
                frontier2.push(Move(neighbor, loc2, new_cost, heuristic2(neighbor)))
    
    # Return None if no maze solution is found
    if return_weights: return None, None, combine_weights(visited_node, visited_node2)
    return None, None


# Dijkstra's Algorithm (A* with zero heuristic)
def dijkstra(maze, return_weights=False):
    """
    Dijkstra's algorithm finds the shortest path using uniform cost search.
    It's essentially A* with a heuristic function that always returns 0.
    """
    # Use A* with zero heuristic
    zero_heuristic = lambda end: lambda loc: 0
    return a_star(maze, zero_heuristic, return_weights)


# Greedy Best-First Search
def greedy_best_first(maze, heuristic_func, return_weights=False):
    """
    Greedy Best-First Search uses only the heuristic to guide the search.
    It doesn't consider the actual path cost, making it faster but not optimal.
    """
    # Initialize a priority queue
    frontier = PriorityQueue()
    heuristic = heuristic_func(maze.end_node)

    # Create initial move with zero cost (we only use heuristic)
    frontier.push(Move(maze.start_node, None, 0.0, heuristic(maze.start_node)))

    # Track visited nodes
    visited_node = {maze.start_node: 0.0}

    # List to store all explored paths
    all_paths = []

    # Main Greedy Best-First loop
    while not frontier.empty:
        loc = frontier.pop()
        active = loc.current
        all_paths.append(active)

        # Check if the end node is reached
        if maze.end_node_line(active):
            final_path = reconstruct_path(loc)
            if return_weights: return final_path[1:], all_paths[1:-1], visited_node
            return final_path[1:], all_paths[1:-1]

        # Explore neighbors
        for neighbor in maze.get_neighbors(active):
            # Only use heuristic for priority, ignore actual cost
            if neighbor not in visited_node:
                visited_node[neighbor] = 0.0  # We don't track actual cost in greedy
                # Push with zero cost, only heuristic matters
                frontier.push(Move(neighbor, loc, 0.0, heuristic(neighbor)))

    # Return None if no maze solution is found
    if return_weights: return None, None, visited_node
    return None, None


# Jump Point Search (JPS) - Optimized A* for uniform-cost grids
def jump_point_search(maze, heuristic_func, return_weights=False):
    """
    Jump Point Search is an optimization of A* for uniform-cost grids.
    It identifies and jumps to key points, significantly reducing nodes explored.
    """

    def jump(current, direction, goal):
        """
        Recursively jump in a direction until hitting a jump point or obstacle.

        Args:
            current: Current coordinate
            direction: (dx, dy) direction tuple
            goal: Goal coordinate

        Returns:
            Jump point coordinate or None if blocked
        """
        next_x = current.x + direction[0]
        next_y = current.y + direction[1]

        # Check bounds
        if next_x < 0 or next_x >= maze.rows or next_y < 0 or next_y >= maze.columns:
            return None

        next_coord = Coordinate(next_x, next_y)

        # Check if blocked by wall
        if maze.maze[next_x][next_y] == MazeSymbol.wall:
            return None

        # Check if reached goal
        if next_coord == goal:
            return next_coord

        # Check for forced neighbors (this makes it a jump point)
        if direction[0] != 0 and direction[1] != 0:  # Diagonal movement
            # Check horizontal and vertical directions
            if (jump(next_coord, (direction[0], 0), goal) is not None or
                jump(next_coord, (0, direction[1]), goal) is not None):
                return next_coord
        else:  # Horizontal or vertical movement
            if direction[0] != 0:  # Horizontal
                # Check for forced neighbors above and below
                if ((next_x + 1 < maze.rows and maze.maze[next_x + 1][next_y] != MazeSymbol.wall and
                     next_x + 1 < maze.rows and next_y - direction[1] >= 0 and
                     maze.maze[next_x + 1][next_y - direction[1]] == MazeSymbol.wall) or
                    (next_x - 1 >= 0 and maze.maze[next_x - 1][next_y] != MazeSymbol.wall and
                     next_x - 1 >= 0 and next_y - direction[1] >= 0 and
                     maze.maze[next_x - 1][next_y - direction[1]] == MazeSymbol.wall)):
                    return next_coord
            else:  # Vertical
                # Check for forced neighbors left and right
                if ((next_y + 1 < maze.columns and maze.maze[next_x][next_y + 1] != MazeSymbol.wall and
                     next_x - direction[0] >= 0 and next_y + 1 < maze.columns and
                     maze.maze[next_x - direction[0]][next_y + 1] == MazeSymbol.wall) or
                    (next_y - 1 >= 0 and maze.maze[next_x][next_y - 1] != MazeSymbol.wall and
                     next_x - direction[0] >= 0 and next_y - 1 >= 0 and
                     maze.maze[next_x - direction[0]][next_y - 1] == MazeSymbol.wall)):
                    return next_coord

        # Recursively continue jumping
        return jump(next_coord, direction, goal)

    def get_successors(current):
        """Get jump point successors for current position."""
        successors = []
        # Try all 4 cardinal directions (JPS works best with 4-directional movement)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for direction in directions:
            jump_point = jump(current, direction, maze.end_node)
            if jump_point:
                successors.append(jump_point)

        return successors

    # Initialize priority queue for JPS
    frontier = PriorityQueue()
    heuristic = heuristic_func(maze.end_node)
    frontier.push(Move(maze.start_node, None, 0.0, heuristic(maze.start_node)))

    # Track visited nodes and their costs
    visited_node = {maze.start_node: 0.0}

    # List to store all explored paths
    all_paths = []

    # Main JPS loop
    while not frontier.empty:
        loc = frontier.pop()
        active = loc.current
        all_paths.append(active)

        # Check if the end node is reached
        if maze.end_node_line(active):
            final_path = reconstruct_path(loc)
            if return_weights: return final_path[1:], all_paths[1:-1], visited_node
            return final_path[1:], all_paths[1:-1]

        # Get jump point successors
        successors = get_successors(active)

        for neighbor in successors:
            # Calculate cost (Manhattan distance between points)
            new_cost = loc.cost + abs(neighbor.x - active.x) + abs(neighbor.y - active.y)

            # Update cost if a shorter path is found
            if neighbor not in visited_node or visited_node[neighbor] > new_cost:
                visited_node[neighbor] = new_cost
                frontier.push(Move(neighbor, loc, new_cost, heuristic(neighbor)))

    # Return None if no maze solution is found
    if return_weights: return None, None, visited_node
    return None, None