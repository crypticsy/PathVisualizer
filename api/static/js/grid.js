/**
 * PathGrid - Interactive 30x30 grid system with drag & drop functionality
 * Handles grid rendering, user interactions, and path visualization
 */
class PathGrid {
    constructor(rows, cols, containerId) {
        this.rows = rows;
        this.cols = cols;
        this.container = document.getElementById(containerId);
        this.cells = [];
        this.animationSpeed = 50; // milliseconds per cell animation

        // Grid state - dynamic end position based on grid size
        this.state = {
            start: [0, 0],
            end: [rows - 1, cols - 1],  // Bottom-right corner dynamically
            walls: new Set(),
            isDragging: false,
            dragMode: null,  // 'start', 'end', 'wall', 'erase'
            currentMarker: null,  // Track which marker is being dragged
        };

        this.init();
    }

    /**
     * Initialize the grid system
     */
    init() {
        this.createGrid();
        this.setupEventListeners();
        this.addHoverEffects();
    }

    /**
     * Create the 30x30 grid using CSS Grid and document fragment for performance
     */
    createGrid() {
        // Clear container
        this.container.innerHTML = '';

        // Setup CSS Grid
        this.container.style.gridTemplateColumns = `repeat(${this.cols}, 1fr)`;
        this.container.style.gridTemplateRows = `repeat(${this.rows}, 1fr)`;

        // Create cells using document fragment for batch DOM insertion
        const fragment = document.createDocumentFragment();

        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const cell = this.createCell(row, col);
                fragment.appendChild(cell);
                this.cells.push(cell);
            }
        }

        this.container.appendChild(fragment);
    }

    /**
     * Create a single grid cell
     */
    createCell(row, col) {
        const cell = document.createElement('div');
        cell.className = 'grid-cell';
        cell.dataset.row = row;
        cell.dataset.col = col;

        // Set initial cell state
        if (row === this.state.start[0] && col === this.state.start[1]) {
            cell.classList.add('cell-start');
            cell.textContent = 'S';
        } else if (row === this.state.end[0] && col === this.state.end[1]) {
            cell.classList.add('cell-end');
            cell.textContent = 'E';
        } else {
            cell.classList.add('cell-empty');
        }

        return cell;
    }

    /**
     * Setup event listeners using event delegation for performance
     */
    setupEventListeners() {
        // Use pointer events for unified mouse/touch support
        this.container.addEventListener('pointerdown', this.handlePointerDown.bind(this));
        this.container.addEventListener('pointermove', this.handlePointerMove.bind(this));
        this.container.addEventListener('pointerup', this.handlePointerUp.bind(this));
        this.container.addEventListener('pointerleave', this.handlePointerUp.bind(this));

        // Prevent context menu on right click
        this.container.addEventListener('contextmenu', (e) => e.preventDefault());
    }

    /**
     * Handle pointer down (mouse down or touch start)
     */
    handlePointerDown(e) {
        const cell = e.target.closest('.grid-cell');
        if (!cell) return;

        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);

        // Check if clicking on start marker
        if (cell.classList.contains('cell-start')) {
            this.state.isDragging = true;
            this.state.dragMode = 'start';
            cell.classList.add('dragging');
            return;
        }

        // Check if clicking on end marker
        if (cell.classList.contains('cell-end')) {
            this.state.isDragging = true;
            this.state.dragMode = 'end';
            cell.classList.add('dragging');
            return;
        }

        // Clear any existing path before drawing walls
        this.clearVisualization();

        // Wall drawing mode
        this.state.isDragging = true;

        if (cell.classList.contains('cell-wall')) {
            this.state.dragMode = 'erase';
            this.removeWall(row, col);
        } else if (cell.classList.contains('cell-empty')) {
            this.state.dragMode = 'wall';
            this.addWall(row, col);
        }
    }

    /**
     * Handle pointer move (mouse move or touch move)
     */
    handlePointerMove(e) {
        if (!this.state.isDragging) return;

        const cell = e.target.closest('.grid-cell');
        if (!cell) return;

        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);

        // Handle marker dragging
        if (this.state.dragMode === 'start') {
            this.moveStart(row, col);
        } else if (this.state.dragMode === 'end') {
            this.moveEnd(row, col);
        }
        // Handle wall drawing/erasing
        else if (this.state.dragMode === 'wall') {
            if (cell.classList.contains('cell-empty')) {
                this.addWall(row, col);
            }
        } else if (this.state.dragMode === 'erase') {
            if (cell.classList.contains('cell-wall')) {
                this.removeWall(row, col);
            }
        }
    }

    /**
     * Handle pointer up (mouse up or touch end)
     */
    handlePointerUp(e) {
        if (this.state.isDragging) {
            // Remove dragging class from all cells
            this.container.querySelectorAll('.dragging').forEach(cell => {
                cell.classList.remove('dragging');
            });

            this.state.isDragging = false;
            this.state.dragMode = null;
        }
    }

    /**
     * Move the start marker to a new position
     */
    moveStart(row, col) {
        // Don't move to end position or wall
        if ((row === this.state.end[0] && col === this.state.end[1]) ||
            this.state.walls.has(`${row},${col}`)) {
            return;
        }

        // Remove start from old position
        const oldCell = this.getCell(this.state.start[0], this.state.start[1]);
        oldCell.classList.remove('cell-start', 'dragging');
        oldCell.classList.add('cell-empty');
        oldCell.textContent = '';

        // Add start to new position
        const newCell = this.getCell(row, col);
        newCell.classList.remove('cell-empty');
        newCell.classList.add('cell-start', 'dragging');
        newCell.textContent = 'S';

        // Update state
        this.state.start = [row, col];
    }

    /**
     * Move the end marker to a new position
     */
    moveEnd(row, col) {
        // Don't move to start position or wall
        if ((row === this.state.start[0] && col === this.state.start[1]) ||
            this.state.walls.has(`${row},${col}`)) {
            return;
        }

        // Remove end from old position
        const oldCell = this.getCell(this.state.end[0], this.state.end[1]);
        oldCell.classList.remove('cell-end', 'dragging');
        oldCell.classList.add('cell-empty');
        oldCell.textContent = '';

        // Add end to new position
        const newCell = this.getCell(row, col);
        newCell.classList.remove('cell-empty');
        newCell.classList.add('cell-end', 'dragging');
        newCell.textContent = 'E';

        // Update state
        this.state.end = [row, col];
    }

    /**
     * Add a wall at the specified position
     */
    addWall(row, col) {
        // Don't allow walls on start or end
        if ((row === this.state.start[0] && col === this.state.start[1]) ||
            (row === this.state.end[0] && col === this.state.end[1])) {
            return;
        }

        const cell = this.getCell(row, col);
        if (!cell.classList.contains('cell-wall')) {
            cell.classList.remove('cell-empty', 'cell-visited', 'cell-path');
            cell.classList.add('cell-wall');
            this.state.walls.add(`${row},${col}`);
        }
    }

    /**
     * Remove a wall at the specified position
     */
    removeWall(row, col) {
        const cell = this.getCell(row, col);
        if (cell.classList.contains('cell-wall')) {
            cell.classList.remove('cell-wall');
            cell.classList.add('cell-empty');
            this.state.walls.delete(`${row},${col}`);
        }
    }

    /**
     * Clear all walls from the grid
     */
    clearWalls() {
        this.state.walls.forEach(wallKey => {
            const [row, col] = wallKey.split(',').map(Number);
            this.removeWall(row, col);
        });
        this.state.walls.clear();
    }

    /**
     * Clear only the visualization (visited and path cells)
     */
    clearVisualization() {
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const cell = this.getCell(row, col);
                cell.classList.remove('cell-visited', 'cell-path');

                // Restore appropriate class
                if (row === this.state.start[0] && col === this.state.start[1]) {
                    // Keep start
                } else if (row === this.state.end[0] && col === this.state.end[1]) {
                    // Keep end
                } else if (this.state.walls.has(`${row},${col}`)) {
                    if (!cell.classList.contains('cell-wall')) {
                        cell.classList.add('cell-wall');
                    }
                } else {
                    if (!cell.classList.contains('cell-empty')) {
                        cell.classList.remove('cell-wall');
                        cell.classList.add('cell-empty');
                    }
                }
            }
        }
    }

    /**
     * Reset the entire grid to initial state
     */
    resetGrid() {
        this.clearWalls();
        this.clearVisualization();

        // Reset start and end to default positions (dynamic based on grid size)
        const defaultEndRow = this.rows - 1;
        const defaultEndCol = this.cols - 1;

        if (this.state.start[0] !== 0 || this.state.start[1] !== 0) {
            this.moveStart(0, 0);
        }
        if (this.state.end[0] !== defaultEndRow || this.state.end[1] !== defaultEndCol) {
            this.moveEnd(defaultEndRow, defaultEndCol);
        }
    }

    /**
     * Animate the pathfinding visualization
     */
    async animatePath(visitedCells, pathCells) {
        // Clear previous visualization
        this.clearVisualization();

        // Animate visited cells
        if (visitedCells && visitedCells.length > 0) {
            await this.animateCells(visitedCells, 'cell-visited');
        }

        // Animate final path
        if (pathCells && pathCells.length > 0) {
            await this.animateCells(pathCells, 'cell-path');
        }
    }

    /**
     * Animate a list of cells with a specific class
     */
    animateCells(cells, className) {
        return new Promise((resolve) => {
            let index = 0;

            const animate = () => {
                if (index >= cells.length) {
                    resolve();
                    return;
                }

                // Animate in batches of 3 for better performance
                const batch = cells.slice(index, index + 3);
                batch.forEach(([row, col]) => {
                    const cell = this.getCell(row, col);
                    // Don't override start/end cells
                    if (!cell.classList.contains('cell-start') &&
                        !cell.classList.contains('cell-end')) {
                        cell.classList.add(className);
                    }
                });

                index += 3;
                setTimeout(animate, this.animationSpeed);
            };

            animate();
        });
    }

    /**
     * Get a cell at the specified position
     */
    getCell(row, col) {
        return this.container.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    }

    /**
     * Get the current maze state as a 2D grid for the API
     */
    getMazeState() {
        const grid = [];

        for (let row = 0; row < this.rows; row++) {
            grid[row] = [];
            for (let col = 0; col < this.cols; col++) {
                // True if wall, false otherwise
                grid[row][col] = this.state.walls.has(`${row},${col}`);
            }
        }

        return {
            grid: grid,
            start: this.state.start,
            end: this.state.end
        };
    }

    /**
     * Load a maze state from data (e.g., from API)
     */
    loadMazeState(data) {
        // Clear current state
        this.clearWalls();
        this.clearVisualization();

        // Load walls
        if (data.grid) {
            for (let row = 0; row < data.grid.length; row++) {
                for (let col = 0; col < data.grid[row].length; col++) {
                    if (data.grid[row][col]) {
                        this.addWall(row, col);
                    }
                }
            }
        }

        // Load start position
        if (data.start) {
            this.moveStart(data.start[0], data.start[1]);
        }

        // Load end position
        if (data.end) {
            this.moveEnd(data.end[0], data.end[1]);
        }
    }

    /**
     * Add visual hover effects to indicate draggability
     */
    addHoverEffects() {
        // Hover effects are handled by CSS
        // This method is for any additional JS-based effects if needed
    }

    /**
     * Update grid size and reinitialize
     */
    updateGridSize(rows, cols) {
        // Store current state
        const oldRows = this.rows;
        const oldCols = this.cols;

        // Update dimensions
        this.rows = rows;
        this.cols = cols;

        // Calculate new default positions for start and end
        const newEndRow = Math.min(this.state.end[0], rows - 1);
        const newEndCol = Math.min(this.state.end[1], cols - 1);
        const newStartRow = Math.min(this.state.start[0], rows - 1);
        const newStartCol = Math.min(this.state.start[1], cols - 1);

        // Reset walls that are out of bounds
        const wallsToKeep = new Set();
        this.state.walls.forEach(wallKey => {
            const [row, col] = wallKey.split(',').map(Number);
            if (row < rows && col < cols) {
                wallsToKeep.add(wallKey);
            }
        });
        this.state.walls = wallsToKeep;

        // Update start and end positions
        this.state.start = [newStartRow, newStartCol];
        this.state.end = [newEndRow, newEndCol];

        // Clear and recreate grid
        this.cells = [];
        this.createGrid();
        this.setupEventListeners();
    }
}
