import numpy as np
from api.maze import Maze, Coordinate
from flask import render_template, Flask, request
from api.algo import depth_first_search, breadth_first_search, a_star, manhattan_distance

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    m = Maze()
    if request.method == 'POST':
        if request.form['rand'] == 'loc':
            rand_x = np.random.choice(np.arange(5))
            rand_y = np.random.choice(np.arange(6)) if rand_x != 0 else np.random.choice(np.arange(1, 6))
            m = Maze(end_node=Coordinate(x=rand_x, y=rand_y))
        elif request.form['rand'] == 'wall':
            m = Maze(random_obstacles=True)
            
    final_dfs, path_dfs = depth_first_search(m.start_node, m.end_node_line, m.get_neighbors)
    if path_dfs is None:
        while path_dfs is None:
            m = Maze()
            final_dfs, path_dfs = depth_first_search(m.start_node, m.end_node_line, m.get_neighbors)
            
    final_bfs, path_bfs = breadth_first_search(m.start_node, m.end_node_line, m.get_neighbors)
    distance = manhattan_distance(m.end_node)
    final_astar, path_astar = a_star(m.start_node, m.end_node_line, m.get_neighbors, distance)
    
    return render_template(
        'home.html', 
        maze_map=m.maze, 
        dfs_path=path_dfs, 
        bfs_path=path_bfs,
        astar_path=path_astar, 
        final_bfs=final_bfs, 
        final_dfs=final_dfs,
        final_astar=final_astar)

test = "234"