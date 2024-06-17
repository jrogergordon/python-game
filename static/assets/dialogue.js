let dialogueTexts = [];
let pastSpeakerIndex = null;
let speakerImages = [];
let speakerNameLabels = [];
let dialogueLines = [];

function processDialogue(dialogue) {
    dialogueTexts = dialogue;
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
        speakerNameLabels = speakerNameLabels.filter(label => label !== nameDiv);
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

function fetchDialogue() {
    return fetch('/static/assets/dialogue_test.txt')
        .then(response => response.text())
        .then(data => data.split('\n'));
}

function startDialogue() {
    fetchDialogue().then(dialogue => processDialogue(dialogue));
}

export default startDialogue;