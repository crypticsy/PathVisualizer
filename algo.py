from queue import PriorityQueue



def manhattan_distance(x1, y1, x2, y2):
    # Simple Manhattan distance heuristic
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_distance(x1, y1, x2, y2):
    # Simple Euclidean distance heuristic
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def heuristic(tile, goal_tile):
    # Heuristic function for A* algorithm
    return manhattan_distance(tile.x, tile.y, goal_tile.x, goal_tile.y)



def reconstruct_path(came_from, current):
    # Reconstruct the path from the search algorithm results
    path = []
    while current in came_from:
        path.append((current.x, current.y))
        current = came_from[current]
    
    path.append((current.x, current.y))  # Add start position
    return path[::-1]  # Reverse the path to start from the beginning



def bfs(maze, visualize=False):
    if maze.start_pos is None or maze.goal_pos is None:
        raise ValueError("Start or goal position not set.")

    start_tile = maze.grid[maze.start_pos[0], maze.start_pos[1]]
    goal_tile = maze.grid[maze.goal_pos[0], maze.goal_pos[1]]

    queue = [start_tile]
    visited = set()
    came_from = {}

    while queue:
        current = queue.pop(0)

        if current == goal_tile:
            return reconstruct_path(came_from, goal_tile)

        if current not in visited:
            visited.add(current)
            
            if visualize:
                maze.grid[current.x, current.y].set_visited()
                print(maze)

            for neighbor_pos in maze.get_neighbors(current.x, current.y):
                neighbor = maze.grid[neighbor_pos[0], neighbor_pos[1]]
                if neighbor not in visited:
                    came_from[neighbor] = current
                    queue.append(neighbor)

    return None  # No path found



def dijkstra(maze, visualize=False):
    if maze.start_pos is None or maze.goal_pos is None:
        raise ValueError("Start or goal position not set.")

    start_tile = maze.grid[maze.start_pos[0], maze.start_pos[1]]
    goal_tile = maze.grid[maze.goal_pos[0], maze.goal_pos[1]]

    queue = [(0, start_tile)]
    visited = set()
    came_from = {}
    g_score = {tile: float('inf') for row in maze.grid for tile in row}
    g_score[start_tile] = 0

    while queue:
        _, current = queue.pop(0)

        if current == goal_tile:
            return reconstruct_path(came_from, goal_tile)

        if current not in visited:
            visited.add(current)
            
            if visualize:
                maze.grid[current.x, current.y].set_visited()
                print(maze)

            for neighbor_pos in maze.get_neighbors(current.x, current.y):
                neighbor = maze.grid[neighbor_pos[0], neighbor_pos[1]]
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    queue.append((tentative_g_score, neighbor))
                    queue.sort(key=lambda x: x[0])

    return None  # No path found



def a_star(maze, visualize=False):
    if maze.start_pos is None or maze.goal_pos is None:
        raise ValueError("Start or goal position not set.")

    start_tile = maze.grid[maze.start_pos[0], maze.start_pos[1]]
    goal_tile = maze.grid[maze.goal_pos[0], maze.goal_pos[1]]

    open_set = PriorityQueue()
    open_set.put((0, start_tile))

    came_from = {}
    g_score = {tile: float('inf') for row in maze.grid for tile in row}
    g_score[start_tile] = 0

    while not open_set.empty():
        current = open_set.get()[1]
        
        if visualize:
            maze.grid[current.x, current.y].set_visited()
            print(maze)

        if current == goal_tile:
            return reconstruct_path(came_from, goal_tile)

        for neighbor_pos in maze.get_neighbors(current.x, current.y):
            neighbor = maze.grid[neighbor_pos[0], neighbor_pos[1]]
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                priority = tentative_g_score + heuristic(neighbor, goal_tile)
                open_set.put((priority, neighbor))

    return None  # No path found
