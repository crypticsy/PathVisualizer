import time
from flask import Blueprint, request, jsonify
from api.maze import Maze, Coordinate
from api.algo import (
    depth_first_search,
    breadth_first_search,
    a_star,
    dijkstra,
    greedy_best_first,
    bidirectional_heuristic_search,
    jump_point_search,
    manhattan_distance
)

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/solve', methods=['POST'])
def solve_maze():
    """
    Execute a pathfinding algorithm on a given maze state.

    Expected JSON payload:
    {
        "algorithm": str,  # "astar", "bfs", "dfs", "dijkstra", "greedy", "bidirectional", "jps"
        "grid": [[bool]],  # 2D array where true = wall, false = empty
        "start": [int, int],  # [row, col]
        "end": [int, int]  # [row, col]
    }

    Returns:
    {
        "success": bool,
        "visited": [[int, int]],  # List of visited coordinates
        "path": [[int, int]],  # Final path coordinates
        "stats": {
            "nodesVisited": int,
            "pathLength": int,
            "timeTaken": float  # milliseconds
        },
        "error": str  # Only if success = false
    }
    """
    try:
        data = request.get_json()

        # Validate request
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        algorithm = data.get('algorithm', 'astar')
        grid_state = data.get('grid')
        start = data.get('start', [0, 0])
        end = data.get('end', [29, 29])

        if not grid_state:
            return jsonify({"success": False, "error": "Grid state not provided"}), 400

        # Create maze from grid state
        maze = Maze.from_grid_state(grid_state, start, end)

        # Select and execute algorithm
        start_time = time.time()

        algorithm_map = {
            'astar': lambda: a_star(maze, manhattan_distance),
            'bfs': lambda: breadth_first_search(maze),
            'dfs': lambda: depth_first_search(maze),
            'dijkstra': lambda: dijkstra(maze),
            'greedy': lambda: greedy_best_first(maze, manhattan_distance),
            'bidirectional': lambda: bidirectional_heuristic_search(maze, manhattan_distance),
            'jps': lambda: jump_point_search(maze, manhattan_distance)
        }

        if algorithm not in algorithm_map:
            return jsonify({
                "success": False,
                "error": f"Unknown algorithm: {algorithm}"
            }), 400

        # Execute algorithm
        final_path, visited_path = algorithm_map[algorithm]()

        end_time = time.time()
        time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

        # Check if path was found
        if final_path is None:
            return jsonify({
                "success": False,
                "error": "No path found between start and end points",
                "stats": {
                    "nodesVisited": len(visited_path) if visited_path else 0,
                    "pathLength": 0,
                    "timeTaken": round(time_taken, 2)
                }
            }), 200

        # Convert Coordinate objects to [row, col] lists
        visited_coords = [[coord.x, coord.y] for coord in visited_path] if visited_path else []
        path_coords = [[coord.x, coord.y] for coord in final_path] if final_path else []

        return jsonify({
            "success": True,
            "visited": visited_coords,
            "path": path_coords,
            "stats": {
                "nodesVisited": len(visited_coords),
                "pathLength": len(path_coords),
                "timeTaken": round(time_taken, 2)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@api_bp.route('/maze/validate', methods=['POST'])
def validate_maze():
    """
    Validate if a maze has a solution.

    Expected JSON payload:
    {
        "grid": [[bool]],
        "start": [int, int],
        "end": [int, int]
    }

    Returns:
    {
        "valid": bool,
        "message": str
    }
    """
    try:
        data = request.get_json()

        grid_state = data.get('grid')
        start = data.get('start', [0, 0])
        end = data.get('end', [29, 29])

        if not grid_state:
            return jsonify({"valid": False, "message": "Grid state not provided"}), 400

        # Create maze and try to find path with BFS (fast)
        maze = Maze.from_grid_state(grid_state, start, end)
        final_path, _ = breadth_first_search(maze)

        if final_path is None:
            return jsonify({
                "valid": False,
                "message": "No path exists between start and end points"
            }), 200

        return jsonify({
            "valid": True,
            "message": "Valid maze with solution"
        }), 200

    except Exception as e:
        return jsonify({
            "valid": False,
            "message": f"Error validating maze: {str(e)}"
        }), 500


@api_bp.route('/maze/generate', methods=['POST'])
def generate_maze():
    """
    Generate a random maze.

    Expected JSON payload:
    {
        "rows": int,
        "cols": int,
        "density": float  # 0.0 to 1.0, percentage of walls
    }

    Returns:
    {
        "grid": [[bool]],  # 2D array where true = wall
        "start": [int, int],
        "end": [int, int]
    }
    """
    try:
        data = request.get_json()

        rows = data.get('rows', 30)
        cols = data.get('cols', 30)
        density = data.get('density', 0.3)

        # Create maze with random obstacles
        maze = Maze(
            rows=rows,
            columns=cols,
            barriers=density,
            random_obstacles=True
        )

        # Ensure maze has a solution, regenerate if needed
        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            final_path, _ = breadth_first_search(maze)
            if final_path is not None:
                break

            # Regenerate maze
            maze = Maze(
                rows=rows,
                columns=cols,
                barriers=density,
                random_obstacles=True
            )
            attempts += 1

        # Convert maze to grid format
        grid = []
        for row in maze.maze:
            grid_row = []
            for cell in row:
                grid_row.append(cell == 'X')  # True if wall
            grid.append(grid_row)

        return jsonify({
            "grid": grid,
            "start": [maze.start_node.x, maze.start_node.y],
            "end": [maze.end_node.x, maze.end_node.y]
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Error generating maze: {str(e)}"
        }), 500
