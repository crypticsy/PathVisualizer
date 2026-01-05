/**
 * Main application initialization
 */
document.addEventListener('DOMContentLoaded', () => {
    // Get initial grid size from inputs
    const gridRows = parseInt(document.getElementById('gridRows').value);
    const gridCols = parseInt(document.getElementById('gridCols').value);

    // Initialize grid
    const grid = new PathGrid(gridRows, gridCols, 'pathGrid');

    // Initialize controls
    const controls = new VisualizerControls(grid);

    // Setup event listeners for UI controls
    setupEventListeners(grid, controls);

    // Setup modal
    setupModal();

    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

/**
 * Setup all event listeners for UI controls
 */
function setupEventListeners(grid, controls) {
    // Run algorithm button
    const runBtn = document.getElementById('runBtn');
    if (runBtn) {
        runBtn.addEventListener('click', () => {
            const algorithm = document.getElementById('algorithmSelect').value;
            controls.runAlgorithm(algorithm);
        });
    }

    // Generate maze button
    const generateMazeBtn = document.getElementById('generateMazeBtn');
    if (generateMazeBtn) {
        generateMazeBtn.addEventListener('click', () => {
            controls.generateMaze();
        });
    }

    // Clear path button
    const clearPathBtn = document.getElementById('clearPathBtn');
    if (clearPathBtn) {
        clearPathBtn.addEventListener('click', () => {
            controls.clearPath();
        });
    }

    // Clear walls button
    const clearWallsBtn = document.getElementById('clearWallsBtn');
    if (clearWallsBtn) {
        clearWallsBtn.addEventListener('click', () => {
            controls.clearWalls();
        });
    }

    // Reset button
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            controls.resetGrid();
        });
    }

    // Speed slider (reversed: high slider value = fast speed)
    const speedSlider = document.getElementById('speedSlider');
    if (speedSlider) {
        speedSlider.addEventListener('input', (e) => {
            // Reverse the value: max slider (200) = min animation delay (10)
            const reversed = 210 - parseInt(e.target.value);
            grid.animationSpeed = reversed;
        });

        // Set initial value (reversed)
        const reversed = 210 - parseInt(speedSlider.value);
        grid.animationSpeed = reversed;
    }

    // Grid size apply button
    const applyGridSizeBtn = document.getElementById('applyGridSize');
    if (applyGridSizeBtn) {
        applyGridSizeBtn.addEventListener('click', () => {
            const rows = parseInt(document.getElementById('gridRows').value);
            const cols = parseInt(document.getElementById('gridCols').value);

            // Validate input
            if (rows < 10 || rows > 50 || cols < 10 || cols > 50) {
                controls.showNotification('Grid size must be between 10 and 50', 'error');
                return;
            }

            // Update grid dimensions
            grid.updateGridSize(rows, cols);
            controls.resetStats();
            controls.showNotification(`Grid resized to ${rows}x${cols}`, 'info');

            // Reinitialize icons after grid is recreated
            if (typeof lucide !== 'undefined') {
                setTimeout(() => lucide.createIcons(), 100);
            }
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ignore if typing in input fields
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
            return;
        }

        // Space to run
        if (e.code === 'Space' && !controls.isRunning) {
            e.preventDefault();
            const algorithm = document.getElementById('algorithmSelect').value;
            controls.runAlgorithm(algorithm);
        }

        // R to reset
        if (e.code === 'KeyR' && !controls.isRunning) {
            e.preventDefault();
            controls.resetGrid();
        }

        // C to clear path
        if (e.code === 'KeyC' && !controls.isRunning) {
            e.preventDefault();
            controls.clearPath();
        }

        // G to generate maze
        if (e.code === 'KeyG' && !controls.isRunning) {
            e.preventDefault();
            controls.generateMaze();
        }
    });
}

/**
 * Setup info modal
 */
function setupModal() {
    const infoBtn = document.getElementById('infoBtn');
    const modal = document.getElementById('infoModal');
    const closeBtn = document.getElementById('closeModal');

    if (infoBtn && modal && closeBtn) {
        // Open modal
        infoBtn.addEventListener('click', () => {
            modal.classList.remove('hidden');
            // Reinitialize icons in modal
            if (typeof lucide !== 'undefined') {
                setTimeout(() => lucide.createIcons(), 50);
            }
        });

        // Close modal
        closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
        });

        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
            }
        });
    }
}
