fetch('/game-state')
    .then(response => response.json())
    .then(gameState => {
        const cells = document.querySelectorAll('.cell');
        cells[gameState.highlighted_cell].classList.add('highlighted');

        document.addEventListener('keydown', () => {
            fetch('/change-highlighted-cell', { method: 'POST' })
                .then(response => response.json())
                .then(gameState => {
                    cells.forEach(cell => cell.classList.remove('highlighted'));
                    cells[gameState.highlighted_cell].classList.add('highlighted');
                });
        });
    });