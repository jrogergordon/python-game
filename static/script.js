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
            const row = Math.floor(index / 9);
            const col = index % 9;
            updateHighlightedCell([row, col]);
        });
    });

    const moveButton = document.getElementById('move-button');

    moveButton.addEventListener('click', () => {
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
            .then(data => {
                console.log(data);
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
        highlightedCell.addEventListener('click', () => {
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


    let dialogueTexts = [];
    let currentSpeaker = '';
    let speakerImages = [];
    let dialogueLines = [];
    let speakerNameLabels = [];

    fetch('/static/assets/dialogue_test.txt')
        .then(response => response.text())
        .then(data => {
            dialogueTexts = data.split('\n');
            processDialogue();
        });

    function processDialogue() {
        const imageButton = document.getElementById('image-button');

        let pastSpeakerIndex = null;

        imageButton.addEventListener('click', () => {
            if (dialogueTexts.length > 0) {
                const line = dialogueTexts.shift();
                if (line.startsWith('currentSpeaker:')) {
                    const parts = line.split(':');
                    const nameAndNumber = parts[1].trim().split(' ');
                    const speakerName = nameAndNumber[0];
                    const imageIndex = parseInt(nameAndNumber[1]);
                    displaySpeakerImage(speakerName, imageIndex);
                    updateSpeakerNameLabel(pastSpeakerIndex, imageIndex);
                    pastSpeakerIndex = imageIndex;
                    clearDialogueLines();
                } else if (line.startsWith('eraseSpeaker')) {
                    const numbers = line.replace('eraseSpeaker ', '').trim().split(' ');
                    numbers.forEach(number => {
                        removeSpeakerImage(parseInt(number));
                    });
                } else {
                    displayDialogueLine(line + '\n'); // add a new line after each line of text
                }
            } else {
                clearAll();
            }
        });
    }

    function displaySpeakerImage(speakerName, imageIndex) {
            const imageName = `${speakerName}Talking.png`;
            const imageDiv = document.createElement('div');
            // imageDiv.style.zIndex = 0
            imageDiv.className = `image-div speaker-${imageIndex}`;
            const image = document.createElement('img');
            image.src = `/static/assets/${imageName}`;
            image.className = 'talking-image';

        // Calculate left position based on image index
        let leftPosition;
        switch (imageIndex) {
            case 0:
                leftPosition = 'calc(50% - 300px)';
                break;
            case 1:
                leftPosition = 'calc(50% - 150px)';
                break;
            case 2:
                leftPosition = 'calc(50% + 150px)';
                break;
            case 3:
                leftPosition = 'calc(50% + 300px)';
                break;
        }

        imageDiv.style.position = 'absolute';
        imageDiv.style.top = '62%';
        imageDiv.style.left = leftPosition;
        imageDiv.style.transform = 'translate(-50%, -50%)';
        imageDiv.appendChild(image);

        document.body.appendChild(imageDiv);
        speakerImages.push(imageDiv);

        const nameLabelContainer = document.createElement('div');
        nameLabelContainer.className = `name-div-${imageIndex} name-div`;
        nameLabelContainer.style.position = 'absolute';
        nameLabelContainer.style.top = '70%'; // Adjusted top position
        nameLabelContainer.style.left = leftPosition;
        nameLabelContainer.style.transform = 'translate(-50%, -50%)';
        nameLabelContainer.style.zIndex = 3; // Set the z-index to a high value

        const speakerNameElement = document.createElement('div');
        speakerNameElement.textContent = speakerName;
        speakerNameElement.style.fontWeight = 'bold'; // Make the speaker name bold
        speakerNameElement.style.textAlign = 'center'; // Center the speaker name
        speakerNameElement.style.top = '120px';

        nameLabelContainer.appendChild(speakerNameElement);
        document.body.appendChild(nameLabelContainer);
        speakerNameLabels.push(nameLabelContainer);

        updateSpeakerNameLabel(pastSpeaker=null, imageIndex);
        pastSpeaker = imageIndex;
    }

    function updateSpeakerNameLabel(pastSpeakerIndex, currSpeakerIndex) {
        if (pastSpeakerIndex !== null) {
            const pastSpeakerNameLabel = document.querySelector(`.name-div-${pastSpeakerIndex}`);
            if (pastSpeakerNameLabel) {
                pastSpeakerNameLabel.style.visibility = 'hidden';
            }
        }
        const currSpeakerNameLabel = document.querySelector(`.name-div-${currSpeakerIndex}`);
        if (currSpeakerNameLabel) {
            currSpeakerNameLabel.style.background = 'rgb(0, 0, 139)';
            currSpeakerNameLabel.style.color = 'white';
            currSpeakerNameLabel.style.borderRadius = '10px';
            currSpeakerNameLabel.style.padding = '5px';
        }
    }

    function displayDialogueLine(line) {
        const textDiv = document.querySelector('.bottom-rectangle-text');
        if (!textDiv) {
            const bottomRectangle = document.querySelector('.bottom-rectangle');
            const newTextDiv = document.createElement('div');
            newTextDiv.className = 'bottom-rectangle-text';
            newTextDiv.style.zIndex = 1;
            bottomRectangle.appendChild(newTextDiv);
        }
        document.querySelector('.bottom-rectangle-text').innerHTML += line + '<br>'; // Use innerHTML to add a new line
        dialogueLines.push(line);
        if (dialogueLines.length > 4) {
            dialogueLines.shift();
            document.querySelector('.bottom-rectangle-text').innerHTML = dialogueLines.join('<br>'); // Remove the oldest line and update the HTML
        }
    }

    function removeSpeakerImage(imageIndex) {
        const imageDiv = document.querySelector(`.speaker-${imageIndex}`);
        if (imageDiv) {
            imageDiv.remove();
            speakerImages.splice(imageIndex, 1);
        }
        const nameDiv = document.querySelector(`.name-div-${imageIndex}`);
        if (nameDiv) {
            nameDiv.remove();
            speakerNameLabels.splice(imageIndex, 1);
        }
    } 

    function clearDialogueLines() {
        document.querySelector('.bottom-rectangle-text').innerHTML = '';
        dialogueLines = [];
    }

    function clearAll() {
        while (speakerImages.length > 0) {
            speakerImages.shift().remove();
        }
        while (speakerNameLabels.length > 0) {
            speakerNameLabels.shift().remove();
        }
        clearDialogueLines();
    }

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

});