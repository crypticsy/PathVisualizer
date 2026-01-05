/**
 * VisualizerControls - Handles UI controls and algorithm execution
 */
class VisualizerControls {
    constructor(grid) {
        this.grid = grid;
        this.isRunning = false;
        this.currentAnimation = null;
    }

    /**
     * Execute a pathfinding algorithm
     */
    async runAlgorithm(algorithmName) {
        if (this.isRunning) {
            console.log('Algorithm already running');
            return;
        }

        this.isRunning = true;
        this.disableControls();

        const startTime = Date.now();
        const mazeState = this.grid.getMazeState();

        try {
            // Make API request
            const response = await fetch('/api/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    algorithm: algorithmName,
                    grid: mazeState.grid,
                    start: mazeState.start,
                    end: mazeState.end
                })
            });

            const result = await response.json();

            if (result.success) {
                // Animate the path
                await this.grid.animatePath(result.visited, result.path);

                // Update statistics
                this.updateStats({
                    nodesVisited: result.stats.nodesVisited,
                    pathLength: result.stats.pathLength,
                    timeTaken: result.stats.timeTaken
                });

                this.showNotification('Path found successfully!', 'success');
            } else {
                this.showNotification(result.error || 'No path found', 'error');
                this.updateStats({
                    nodesVisited: result.stats?.nodesVisited || 0,
                    pathLength: 0,
                    timeTaken: result.stats?.timeTaken || 0
                });
            }

        } catch (error) {
            console.error('Error running algorithm:', error);
            this.showNotification('Error executing algorithm', 'error');
        } finally {
            this.isRunning = false;
            this.enableControls();
        }
    }

    /**
     * Generate a random maze
     */
    async generateMaze() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.disableControls();

        try {
            const response = await fetch('/api/maze/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    rows: this.grid.rows,
                    cols: this.grid.cols,
                    density: 0.3
                })
            });

            const result = await response.json();

            if (result.grid) {
                // Load the generated maze
                this.grid.loadMazeState(result);
                this.showNotification('Maze generated successfully!', 'success');
            }

        } catch (error) {
            console.error('Error generating maze:', error);
            this.showNotification('Error generating maze', 'error');
        } finally {
            this.isRunning = false;
            this.enableControls();
        }
    }

    /**
     * Clear only the path visualization
     */
    clearPath() {
        this.grid.clearVisualization();
        this.resetStats();
        this.showNotification('Path cleared', 'info');
    }

    /**
     * Clear all walls from the grid
     */
    clearWalls() {
        this.grid.clearWalls();
        this.grid.clearVisualization();
        this.resetStats();
        this.showNotification('Walls cleared', 'info');
    }

    /**
     * Reset the entire grid
     */
    resetGrid() {
        this.grid.resetGrid();
        this.resetStats();
        this.showNotification('Grid reset', 'info');
    }

    /**
     * Update statistics display
     */
    updateStats(stats) {
        const nodesEl = document.getElementById('nodesVisited');
        const pathEl = document.getElementById('pathLength');
        const timeEl = document.getElementById('timeTaken');

        if (nodesEl) nodesEl.textContent = stats.nodesVisited;
        if (pathEl) pathEl.textContent = stats.pathLength;
        if (timeEl) timeEl.textContent = `${stats.timeTaken}ms`;
    }

    /**
     * Reset statistics to zero
     */
    resetStats() {
        this.updateStats({
            nodesVisited: 0,
            pathLength: 0,
            timeTaken: 0
        });
    }

    /**
     * Disable control buttons during execution
     */
    disableControls() {
        const buttons = [
            'runBtn',
            'generateMazeBtn',
            'clearPathBtn',
            'clearWallsBtn',
            'resetBtn',
            'algorithmSelect'
        ];

        buttons.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.disabled = true;
            }
        });
    }

    /**
     * Enable control buttons after execution
     */
    enableControls() {
        const buttons = [
            'runBtn',
            'generateMazeBtn',
            'clearPathBtn',
            'clearWallsBtn',
            'resetBtn',
            'algorithmSelect'
        ];

        buttons.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.disabled = false;
            }
        });
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} fade-in`;

        // Set colors based on type
        const colors = {
            success: 'bg-nord-aurora-green',
            error: 'bg-nord-aurora-red',
            info: 'bg-nord-frost-3'
        };

        notification.className += ` ${colors[type] || colors.info} text-white px-6 py-3 rounded-lg shadow-lg fixed top-4 right-4 z-50`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}
