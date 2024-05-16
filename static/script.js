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

        if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
            event.preventDefault();
            let direction;
            if (event.key === 'ArrowUp') {
                direction = 'up';
            } else if (event.key === 'ArrowDown') {
                direction = 'down';
            } else if (event.key === 'ArrowLeft') {
                direction = 'left';
            } else if (event.key === 'ArrowRight') {
                direction = 'right';
            }
            updateHighlightedCell(direction);
        }
    });

    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.addEventListener('click', () => {
            spacePressed = false;
            const blueCells = document.querySelectorAll('.blue');
            blueCells.forEach(cell => {
                cell.classList.remove('blue');
            });
            const row = Math.floor(index / 9);
            const col = index % 9;
            updateHighlightedCell([row, col]);
        });
    });

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
                        const highlightedNodeShow = document.getElementById('highlighted-node-show');
                        highlightedNodeShow.innerText = cell.innerText;
                    } else {
                        cell.classList.remove('highlighted');
                    }
                });
            });
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


    let dialogueIndex = 0;
    let dialogueTexts = [];
    let currentSpeaker = '';

    fetch('/static/assets/dialogue_test.txt')
        .then(response => response.text())
        .then(data => {
            dialogueTexts = data.split('\n');
        });

    const dialogueDiv = document.querySelector('.dialogue_text');
    const talkingImageDiv = document.querySelector('.image-div');
    const talkingImage = talkingImageDiv.querySelector('img.talking-image');
    const imageButton = document.getElementById('image-button');

    function displaySpeakerImage(speaker) {
        const imageName = `${speaker}Talking.png`;
        talkingImage.src = `/static/assets/${imageName}`;
    }

    imageButton.addEventListener('click', () => {
        if (dialogueIndex < dialogueTexts.length) {
            const dialogueLine = dialogueTexts[dialogueIndex];
            if (dialogueLine.startsWith('currentSpeaker:')) {
                currentSpeaker = dialogueLine.split(':')[1].trim();
                dialogueDiv.innerHTML = '';
                const speakerLine = document.createElement('div');
                speakerLine.textContent = currentSpeaker;
                speakerLine.style.position = 'absolute';
                speakerLine.style.top = '50%';
                speakerLine.style.left = '50%';
                speakerLine.style.transform = 'translate(-50%, -50%)';
                speakerLine.style.fontSize = 'larger';
                speakerLine.style.fontWeight = 'bold';
                dialogueDiv.appendChild(speakerLine);
                displaySpeakerImage(currentSpeaker);
            } else {
                if (dialogueDiv.children.length > 4) {
                    dialogueDiv.removeChild(dialogueDiv.children[1]);
                }
                const newLine = document.createElement('div');
                newLine.textContent = dialogueLine;
                dialogueDiv.appendChild(newLine);
            }
            dialogueIndex++;
        }
    });
});