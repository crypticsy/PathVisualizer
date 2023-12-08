import numpy as np
from api.maze import Maze, Coordinate
from flask import render_template, Flask, request
from api.algo import depth_first_search, breadth_first_search, a_star, manhattan_distance, bidirectional_heuristic_search

# initialize the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Create a maze object
    m = Maze()

    # Check if the request method is POST
    if request.method == 'POST':
        # Check if the 'rand' parameter in the form is 'loc'
        if request.form['rand'] == 'loc':
            # Generate random coordinates for the end node within the maze bounds
            rand_x = np.random.choice(np.arange(5))
            rand_y = np.random.choice(np.arange(6)) if rand_x != 0 else np.random.choice(np.arange(1, 6))
            
            print(rand_x, rand_y)
            
            # Create a new maze with the specified end node
            m = Maze(end_node=Coordinate(x=rand_x, y=rand_y))
        
        # Check if the 'rand' parameter in the form is 'wall'
        elif request.form['rand'] == 'wall':
            # Create a new maze with random obstacles
            m = Maze(random_obstacles=True)
    
    # Perform depth-first search algorithm on the maze
    final_dfs, path_dfs = depth_first_search(m)

    # If no path is found, regenerate the maze until a valid path is found
    if path_dfs is None:
        while path_dfs is None:
            m = Maze()
            final_dfs, path_dfs = depth_first_search(m)
    
    # Perform breadth-first search algorithm on the maze
    final_bfs, path_bfs = breadth_first_search(m)
    
    # Perform A* search algorithm on the maze
    final_astar, path_astar = a_star(m, manhattan_distance)
    
    # Perform bidirectional A* search algorithm on the maze
    final_bidir, path_bidir = bidirectional_heuristic_search(m, manhattan_distance)
    
    print(final_bidir, path_bidir)
    
    # Render the template with maze information and algorithm results
    return render_template(
        'home.html', 
        maze_map=m.maze, 
        dfs_path=path_dfs, 
        bfs_path=path_bfs,
        astar_path=path_astar, 
        bidir_path=path_bidir,
        final_bfs=final_bfs, 
        final_dfs=final_dfs,
        final_astar=final_astar, 
        final_bidir=final_bidir)