import startDialogue from './assets/dialogue.js';

document.addEventListener('DOMContentLoaded', function () {
    let spacePressed = false;
    
    document.addEventListener('keydown', function (event) {
        if (event.key === ' ') {
            const highlightedCell = document.querySelector('.highlighted');
            if (highlightedCell.dataset.occupant != 0) {
                spacePressed = !spacePressed;
                const blueCells = document.querySelectorAll('.blue');
                blueCells.forEach(cell => {
                    cell.classList.remove('blue');
                });
                const orangeCells = document.querySelectorAll('.orange');
                orangeCells.forEach(cell => {
                    cell.classList.remove('orange');
                });
                if (spacePressed) {
                    const row = highlightedCell.dataset.row;
                    const col = highlightedCell.dataset.col;
                    fetch('/get_reachable_cells', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            row: parseInt(row),
                            col: parseInt(col)
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            data.reachable_cells.forEach(cell => {
                                const cellElement = document.querySelector(`[data-row="${cell[0]}"][data-col="${cell[1]}"]`);
                                cellElement.classList.add('blue');
                            });
                            data.edge_cells.forEach(cell => {
                                const cellElement = document.querySelector(`[data-row="${cell[0]}"][data-col="${cell[1]}"]`);
                                if (cellElement) {
                                    cellElement.classList.add('orange');
                                }
                            });
                        });
                }
            }
        }

        if (event.key === ' ' && spacePressed) {
            const highlightedCell = document.querySelector('.highlighted');
            const row = highlightedCell.dataset.row;
            const col = highlightedCell.dataset.col;
            const newHighlightedCell = document.querySelector('.blue:hover');
            if (newHighlightedCell) {
                const newRow = newHighlightedCell.dataset.row;
                const newCol = newHighlightedCell.dataset.col;
                fetch('/move_character', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        character: game_board.board[row][col].occupant,
                        new_x: newRow,
                        new_y: newCol
                    })
                })
                    .then(response => response.json())
                    .then(() => {
                        spacePressed = false;
                        const blueCells = document.querySelectorAll('.blue');
                        blueCells.forEach(cell => {
                            cell.classList.remove('blue');
                        });
                        const orangeCells = document.querySelectorAll('.orange');
                        orangeCells.forEach(cell => {
                            cell.classList.remove('orange');
                        });
                        updateHighlightedCell([newRow, newCol]);
                    });
            }
        }

        if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
            event.preventDefault();
            let direction;
            if (event.key === 'ArrowUp') {
                direction = 'left'; // Changed from 'up' to 'left'
            } else if (event.key === 'ArrowDown') {
                direction = 'right'; // Changed from 'down' to 'right'
            } else if (event.key === 'ArrowLeft') {
                direction = 'up'; // Changed from 'left' to 'up'
            } else if (event.key === 'ArrowRight') {
                direction = 'down'; // Changed from 'right' to 'down'
            }
            updateHighlightedCell(direction);
        }
    });

    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.addEventListener('click', () => {
            const row = Math.floor(index / 9);
            const col = index % 9;
            updateHighlightedCell([row, col]);
        });
    });


    // Helper function to create a single attribute div
    function createSingleAttributeDiv(attributeName, attributeValue) {
        const attributeDiv = document.createElement('div');
        attributeDiv.classList.add(`${attributeName}-div`);

        const attributeNameDiv = document.createElement('div');
        attributeNameDiv.textContent = attributeName;
        attributeNameDiv.style.textDecoration = 'underline';

        const attributeValueDiv = document.createElement('div');
        attributeValueDiv.textContent = attributeValue;

        attributeDiv.appendChild(attributeNameDiv);
        attributeDiv.appendChild(attributeValueDiv);

        return attributeDiv;
    }

    // Helper function to create character info divs
    function createCharacterInfoDivs(occupant) {
        const highCharAttr = document.createElement('div');
        highCharAttr.classList.add('character-attributes');

        const strengthDiv = createSingleAttributeDiv('Strength', occupant.strength);
        const speedDiv = createSingleAttributeDiv('Speed', occupant.speed);
        const skillDiv = createSingleAttributeDiv('Skill', occupant.skill);
        const defenseDiv = createSingleAttributeDiv('Defense', occupant.defense);

        highCharAttr.appendChild(strengthDiv);
        highCharAttr.appendChild(speedDiv);
        highCharAttr.appendChild(skillDiv);
        highCharAttr.appendChild(defenseDiv);

        const highlightedCharacterShow = document.createElement('div');
        highlightedCharacterShow.classList.add('highlighted-node-character-show');

        const highCharName = document.createElement('div');
        highCharName.classList.add('character-name');
        highCharName.textContent = occupant.name;

        const highCharHealth = document.createElement('div');
        highCharHealth.classList.add('character-health');
        const healthBar = '|'.repeat(occupant.health);
        const wrappedHealthBar = [];

        for (let i = 0; i < healthBar.length; i += 50) {
            wrappedHealthBar.push(healthBar.substring(i, i + 50));
        }

        highCharHealth.innerHTML = `Health <br> <div class="health-bar">${wrappedHealthBar.join('<br>')}</div>`;

        highlightedCharacterShow.appendChild(highCharName);
        highlightedCharacterShow.appendChild(highCharHealth);
        highlightedCharacterShow.appendChild(highCharAttr);

        const rightRectangle = document.querySelector('.right-rectangle');
        rightRectangle.appendChild(highlightedCharacterShow);
    }

    // Helper function to destroy character info divs
    function destroyCharacterInfoDivs() {
        const highCharAttr = document.querySelector('.character-attributes');
        if (highCharAttr) {
            highCharAttr.remove();
        }

        const highlightedCharacterShow = document.querySelector('.highlighted-node-character-show');
        if (highlightedCharacterShow) {
            highlightedCharacterShow.remove();
        }
    }

    // Helper function to create highlighted node show div
    function createHighlightedNodeShowDiv(occupant) {
        const highlightedNodeShow = document.createElement('div');
        highlightedNodeShow.classList.add('bottom-rectangle-text');
        highlightedNodeShow.innerText = occupant.show;

        const rightRectangle = document.querySelector('.right-rectangle');
        rightRectangle.appendChild(highlightedNodeShow);
    }

    // Helper function to destroy highlighted node show div
    function destroyHighlightedNodeShowDiv() {
        const highlightedNodeShow = document.querySelector('.bottom-rectangle-text');
        if (highlightedNodeShow) {
            highlightedNodeShow.remove();
        }
    }
    
    function updateHighlightedCell(directionOrCell) {
        fetch('/update_highlighted_cell', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(typeof directionOrCell === 'string' ? { direction: directionOrCell } : { highlighted_cell: directionOrCell })
        })
            .then(response => response.json())
            .then(data => {
                cells.forEach((cell, index) => {
                    const row = Math.floor(index / 9);
                    const col = index % 9;
                    if (row === data.highlighted_cell[0] && col === data.highlighted_cell[1]) {
                        cell.classList.add('highlighted');

                        // Fetch the occupant of the highlighted cell from the server
                        fetch('/get_occupant', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ row: row, col: col })
                        })
                            .then(response => response.json())
                            .then(occupant => {
                                destroyCharacterInfoDivs();
                                destroyHighlightedNodeShowDiv();

                                if (occupant.type === 'character') {
                                    createCharacterInfoDivs(occupant);
                                } else {
                                    createHighlightedNodeShowDiv(occupant);
                                }
                            });
                    } else {
                        cell.classList.remove('highlighted');
                    }
                });
            });
        const highlightedCell = document.querySelector('.highlighted');
    }

    updateHighlightedCell([0, 0]);

    const dropdownLinks = document.querySelectorAll('.dropdown-content a');

    dropdownLinks.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            const borderIntensity = event.target.dataset.borderIntensity;
            const gridCells = document.querySelectorAll('.cell');
            gridCells.forEach(cell => {
                if (borderIntensity === '0') {
                    cell.style.borderWidth = '0px';
                } else if (borderIntensity === '1') {
                    cell.style.borderWidth = '1px';
                } else if (borderIntensity === '2') {
                    cell.style.borderWidth = '2px';
                }
            });
        });
    });

    startDialogue();

    document.addEventListener('keydown', (event) => {
        if (event.key === ' ' && spacePressed) {
            const highlightedCell = document.querySelector('.highlighted');
            const row = highlightedCell.dataset.row;
            const col = highlightedCell.dataset.col;
            fetch('/move_character', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    character: game_board.board[row][col].occupant,
                    new_x: row,
                    new_y: col
                })
            })
                .then(response => response.json())
                .then(() => {
                    spacePressed = false;
                    const blueCells = document.querySelectorAll('.blue');
                    blueCells.forEach(cell => {
                        cell.classList.remove('blue');
                    });
                    const orangeCells = document.querySelectorAll('.orange');
                    orangeCells.forEach(cell => {
                        cell.classList.remove('orange');
                    });
                });
        }
    });

    fetch('/get_board')
        .then(response => response.json())
        .then(data => populateBoard(data.board));

    function populateBoard(board) {
        const cells = document.querySelectorAll('.cell'); // Move this line here
        for (let i = 0; i < board.length; i++) {
            for (let j = 0; j < board[i].length; j++) {
                const node = board[i][j];
                const htmlNode = document.getElementById(`${j}_${i}`);
                if (node.occupant) {
                    htmlNode.textContent = node.occupant;
                } else {
                    htmlNode.textContent = node.show;
                }
                // Add event listeners to each cell
                htmlNode.addEventListener('click', () => {
                    const row = htmlNode.dataset.row;
                    const col = htmlNode.dataset.col;
                    updateHighlightedCell([parseInt(row), parseInt(col)]);
                });
            }
        }
        updateHighlightedCell([0, 0]); // Highlight the first cell by default
    }
    

});