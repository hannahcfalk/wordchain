// Reference: https://github.com/kubowania/wordle-javascript
// https://www.youtube.com/watch?v=mpby4HiElek
// https://www.youtube.com/watch?v=j7OhcuZQ-q8

// Get HTML classes
const tileDisplay = document.querySelector('.tile-container')
const messageDisplay = document.querySelector('.message-container')
const homeButton = document.getElementById("home")
const clearButton = document.getElementById("clear")
const checkButton = document.getElementById("check")
const scoreDisplay = document.querySelector(".score-container")
const modalDisplay = document.getElementById("game-modal")
const modalContent = document.querySelector(".modal-content")

// Test answer key
test_answer_key = ['TRAIN', 'TRACK', 'TEAM', 'BUILDING', 'BLOCK', 'HEAD']

// Tile layout
const guessRows = [
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],
]

// Variables
let score = 0
let perfect_guess_score = 10
let incorrect_penalty = 1
let possible_points = perfect_guess_score
let currentRow = 1
let currentTile = 0
let isGameOver = false

// Create each of the tiles
guessRows.forEach((guessRow, guessRowIndex) => {
    const rowElement = document.createElement('div')
    rowElement.setAttribute('id', 'guessRow-' + guessRowIndex)
    guessRow.forEach((_guess, guessIndex) => {
        const tileElement = document.createElement('div')
        tileElement.setAttribute('id', 'guessRow-' + guessRowIndex + '-tile-' + guessIndex)
        tileElement.classList.add('tile')
        rowElement.append(tileElement)
    })
    tileDisplay.append(rowElement)
})

// Add starting words
const addStartingWord = (index) => {
    for (let i = 0; i < test_answer_key[index].length; i++){
        const tile = document.getElementById('guessRow-' + index + '-tile-' + i)
        let letter = test_answer_key[index][i]
        tile.textContent = letter
        guessRows[index][i] = letter
        tile.setAttribute('data', letter)
    }
}
addStartingWord(0)
addStartingWord(5)


// Add key listener to page (only trigger if letter or backspace or enter)
document.addEventListener('keydown', function (e) {
    if(!isGameOver){
        if ((e.key).match('^[a-z]{1}$')) {
            addLetter(e.key.toUpperCase())
        }
        if((e.key).match('^Backspace{1}$')){
            addLetter(e.key)
        }
        if((e.key).match('^Enter{1}$')){
            checkRow()
        }
    }
})

// Display letter in tile layout
const addLetter = (letter) => {
    if (currentTile < 13 && currentRow < 6) {
        const tile = document.getElementById('guessRow-' + currentRow + '-tile-' + currentTile)
        if (letter == 'Backspace'){
            deleteLetter()
        }else{
            tile.textContent = letter
            guessRows[currentRow][currentTile] = letter
            tile.setAttribute('data', letter)
            currentTile++
        }
    }
}

// Delete letter when backspace pressed on keyboard
const deleteLetter = () => {
    if (currentTile > 0) {
        currentTile--
        const tile = document.getElementById('guessRow-' + currentRow + '-tile-' + currentTile)
        tile.textContent = ''
        guessRows[currentRow][currentTile] = ''
        tile.setAttribute('data', '')
    }
}

// Display message
const showMessage = (message) => {
    const messageElement = document.createElement('p')
    messageElement.textContent = message
    messageDisplay.append(messageElement)
    setTimeout(() => messageDisplay.removeChild(messageElement), 2000)
}

// Flip tiles when answer entered
const flipTile = (answer) => {
    const rowTiles = document.querySelector('#guessRow-' + currentRow).childNodes
    let checkAnswer = answer
    const guess = []

    rowTiles.forEach((tile, index) => {
        setTimeout(() => {
            tile.classList.add('flip')
        }, 50 * index)
    })
}

// Shake tiles when answer entered
const shakeTile = (answer) => {
    const rowTiles = document.querySelector('#guessRow-' + currentRow).childNodes
    let checkAnswer = answer
    const guess = []

    rowTiles.forEach((tile, index) => {
        tile.classList.add('shake')
        setTimeout(() => {
            tile.classList.remove('shake')
        }, 50)
    })    
}

// Clickable check button
checkButton.addEventListener('click', () => handleCheckClick())
const handleCheckClick = () => {
    if(!isGameOver){
        checkRow()
    }
}

// Checks current row
const checkRow = () => {
    const guess = guessRows[currentRow].join('')
    if(guess == test_answer_key[currentRow]){
        flipTile(test_answer_key[currentRow])
        showMessage('Word Correct!')
        // createModalMessage('Correct! Where do you want your next letter?')
        // createModalButtons()
        // modalDisplay.style.display = 'block'
        currentRow++
        currentTile = 0
        score += possible_points
        updateScore(score)
        possible_points = perfect_guess_score
    }else{
        if(possible_points != 0){
            possible_points -= incorrect_penalty
        }
        shakeTile(test_answer_key[currentRow])
        showMessage('Incorrect!')
        // clearRow(currentRow)
        // createModalMessage('Incorrect! Where do you want your next letter?')
        // createModalButtons()
        // modalDisplay.style.display = 'block'
    }
    if(currentRow == 5){
        isGameOver = true
        showMessage('Game over!')
        // createModalMessage('Game over! Your score was ' + score)
        // modalDisplay.style.display = 'block'
        return
    }
}

// Clear button
clearButton.addEventListener('click', () => handleClearClick())
const handleClearClick = () => {
    if(!isGameOver){
        clearRow(currentRow)
    }
}

// Clear row
const clearRow = (index) => {
    for (let i = 0; i < guessRows[index].length; i++){
        const tile = document.getElementById('guessRow-' + index + '-tile-' + i)
        tile.textContent = ''
        guessRows[index][i] = ''
        tile.setAttribute('data', '')
    }  
    currentTile = 0
}

// Updates score
// Cool feature: a +[score increase] that fades
const updateScore = (updated_score) => {
    const score = document.getElementById('score')
    score.innerHTML = "Score: " + updated_score
}

// Modal message
const createModalMessage = (checkRowMessage) => {
    const modalElement = document.createElement('p')
    modalElement.textContent = checkRowMessage
    modalContent.append(modalElement)
}

// Modal buttons
const createModalButtons = () => {
    let firstWord = test_answer_key[0]
    let sixthWord = test_answer_key[1]
    const modalButton1 = document.createElement('button')
    const modalButton2 = document.createElement('button')
    modalButton1.innerHTML = "Below " + firstWord
    modalButton2.innerHTML = "Above " + sixthWord
    modalButton1.classList.add('modal-button')
    modalButton2.classList.add('modal-button')
    modalContent.append(modalButton1)
    modalContent.append(modalButton2)
}

/*
each wrong guess gets option from bottom or top
can work towards

only answer through row that got most recent letter

if get all guesses wrong, gameover




*/