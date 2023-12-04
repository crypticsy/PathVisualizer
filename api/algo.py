from math import sqrt
from collections import deque
from heapq import heappush, heappop

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


# Define the bidirectional A* search algorithm
def bidirectional_a_star(maze, heuristic_func, return_weights=False):
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
                while frontier2.empty == False:
                    loc2 = frontier2.pop()
                    if loc2.current in visited_node: break
            else:
                while frontier.empty == False:
                    loc = frontier.pop()
                    if loc.current in visited_node2: break
            
            # Combine paths and reverse the path from the end to meeting point
            actual_final_path = reconstruct_path(loc)[1:] + reconstruct_path(loc2)[1:][::-1]
            
            # Return the final path and additional information if requested
            if return_weights: return actual_final_path, all_paths[2:-2], combine_weights(visited_node, visited_node2)
            return actual_final_path, all_paths[2:-2]
        
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
