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

    fetch('/static/assets/dialogue_test.txt')
        .then(response => response.text())
        .then(data => {
            dialogueTexts = data.split('\n');
            processDialogue();
        });

    function processDialogue() {
        const imageButton = document.getElementById('image-button');

        imageButton.addEventListener('click', () => {
            if (dialogueTexts.length > 0) {
                const line = dialogueTexts.shift();
                if (line.startsWith('currentSpeaker:')) {
                    const parts = line.split(':');
                    const nameAndNumber = parts[1].trim().split(' ');
                    const speakerName = nameAndNumber[0];
                    const imageIndex = parseInt(nameAndNumber[1]);
                    displaySpeakerImage(speakerName, imageIndex);
                    clearDialogueLines();
                } else if (line.startsWith('eraseSpeaker')) {
                    const numbers = line.replace('eraseSpeaker ', '').trim().split(' ');
                    numbers.forEach(number => {
                        removeSpeakerImage(parseInt(number));
                    });
                } else {
                    displayDialogueLine(line);
                }
            } else {
                clearAll();
            }
        });
    }

    function displaySpeakerImage(speakerName, imageIndex) {
        const imageName = `${speakerName}Talking.png`;
        const imageDiv = document.createElement('div');
        imageDiv.className = `image-div speaker-${imageIndex}`;
        const image = document.createElement('img');
        image.src = `/static/assets/${imageName}`;
        image.className = 'talking-image';
        imageDiv.appendChild(image);

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
        imageDiv.style.top = '62%'; // Adjusted top position
        imageDiv.style.left = leftPosition;
        imageDiv.style.transform = 'translate(-50%, -50%)';

        document.body.appendChild(imageDiv);
        speakerImages.push(imageDiv);
        const speakerNameElement = document.createElement('div');
        speakerNameElement.textContent = speakerName;
        speakerNameElement.style.fontWeight = 'bold'; // Make the speaker name bold
        speakerNameElement.style.textAlign = 'center'; // Center the speaker name
        speakerNameElement.style.top = '100px'; // Create a new stacking context
        speakerNameElement.style.position = 'absolute'; // Create a new stacking context
        speakerNameElement.style.zIndex = 1000; // Set the z-index to a high value
        imageDiv.appendChild(speakerNameElement);
    }

    function displayDialogueLine(line) {
        const textDiv = document.querySelector('.bottom-rectangle-text');
        if (!textDiv) {
            const bottomRectangle = document.querySelector('.bottom-rectangle');
            const newTextDiv = document.createElement('div');
            newTextDiv.className = 'bottom-rectangle-text';
            newTextDiv.style.zIndex = 1; // Set the z-index of the text to 1
            bottomRectangle.appendChild(newTextDiv);
        }
        const newLine = document.createElement('div');
        newLine.textContent = line;
        newLine.style.whiteSpace = 'pre-wrap'; // Preserve newline characters
        document.querySelector('.bottom-rectangle-text').appendChild(newLine);
        dialogueLines.push(newLine);
        if (dialogueLines.length > 4) {
            dialogueLines.shift().remove();
        }
    }

    function removeSpeakerImage(imageIndex) {
        const imageDiv = document.querySelector(`.speaker-${imageIndex}`);
        if (imageDiv) {
            imageDiv.remove();
            speakerImages.splice(imageIndex, 1);
        }
    }

    function clearDialogueLines() {
        while (dialogueLines.length > 0) {
            dialogueLines.shift().remove();
        }
    }

    function clearAll() {
        while (speakerImages.length > 0) {
            speakerImages.shift().remove();
        }
        clearDialogueLines();
    }
});