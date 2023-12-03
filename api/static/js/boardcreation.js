// 6 array variables representing search paths have been passed to a separate script by the python backend
// including: final_bfs, bfs_path, final_astar... etc.

var b = jsboard.board({ attach: "game", size: "5x6"});

// Maze Symbols
const wall = jsboard.piece({ text: "wall "});
const path = jsboard.piece({ text: "bg-slate-500 path" });
const start = jsboard.piece({ text: "bg-slate-400 " });
const finish = jsboard.piece({ text: "bg-red-400 " });
const empty = jsboard.piece({ text: "empty " });

const rowLookup = {
  X: wall,
  S: start,
  E: finish,
  '*': path
};

function drawMaze(){
    maze_map.forEach(function(row, xAxis){
        row.forEach(function(value, yAxis){
            const symbol = rowLookup[value] || empty;
            b.cell([xAxis, yAxis]).place(symbol.clone());
            });
        });
    };


drawMaze();

// to allow each function to finish, ensure that a delay is as long as the timeout
var lastClick = 0;
var delay = 0;

// The timeout is present to slow down the visualization of the path drawing
function draw(vistedPath, finalPath ){
  if (lastClick >= (Date.now() - delay)) {
    return;
  };
  lastClick = Date.now();
  delay = 150 * vistedPath.length + 150 * finalPath.length;

  drawMaze();

  vistedPath.forEach((coord, index) => {
    setTimeout(() => {
      b.cell([coord[0], coord[1]]).place(path.clone());
      }, 150 * (index + 1));
  });

  finalPath.forEach((coord, index) => {
    setTimeout(() => {
      b.cell([coord[0], coord[1]]).place(path.clone("final"));
      }, 150 * (index + 1) + 150 * vistedPath.length);
  });
};

// Draw Search Paths
document.getElementById("drawPathDFS").addEventListener("click", () => draw(dfs_path, final_dfs));
document.getElementById("drawPathBFS").addEventListener("click", () => draw(bfs_path, final_bfs));
document.getElementById("drawPathAstar").addEventListener("click", () => draw(astar_path, final_astar));