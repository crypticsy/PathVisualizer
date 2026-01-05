# Path Visualizer

[![Website](https://badgen.net/badge/Website/vercel.app/green)](https://path-visualizer-crypticsy.vercel.app/)

A python project to visualize search algorithms on a grid. This project is built using the flask framework and the front-end is built using HTML, CSS and JavaScript, as well as uses tailwindcss for styling. 

<br/>
<div align="center" style="flex-direction: column;">
  <img src="./demo.gif" alt="System Demo" width="100%"/>
  <div style="font-size: 0.8em; color: gray;">Demo</div>
</div>

<br/>

The search algorithms implemented are:
- Breadth First Search
- Depth First Search
- A* Search Algorithm (using the Manhattan distance heuristic)
- Bidirectional A* Search
- Dijkstra's Algorithm
- Greedy Best-First Search
- Jump Point Search
<br/>

## Setup

Create a separate conda environment with the python version 3.9 using the following command:

```shell
conda create -n pathVisualizer python=3.9
```

then activate the environment:

```shell
conda activate pathVisualizer
```
 
and install the required libraries using the following command:

```shell
pip install -r requirements.txt
```
<br/>

## Usage

```shell
# activate the conda environment
conda activate pathVisualizer

# run the flask application
python run.py
```