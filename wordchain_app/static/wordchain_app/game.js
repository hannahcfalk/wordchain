// Reference: https://github.com/kubowania/wordle-javascript
// https://www.youtube.com/watch?v=mpby4HiElek
// https://www.youtube.com/watch?v=j7OhcuZQ-q8

// Get HTML elements
const tileDisplay = document.querySelector('.tile-container')
const messageDisplay = document.querySelector('.message-container')
const homeButton = document.getElementById("home")
const clearButton = document.getElementById("clear")
const checkButton = document.getElementById("check")
const scoreDisplay = document.querySelector(".score-container")
const modalDisplay = document.getElementById("game-modal")
const modalContent = document.querySelector(".modal-content")

// Test answer key and level
let test_answer_key = ['TRAIN', 'TRACK', 'TEAM', 'BUILDING', 'BLOCK', 'HEAD']
let level = 1

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
let perfect_guess_score = 0
if(level == 1){
    perfect_guess_score = 10 
}else if(level == 2){
    perfect_guess_score = 20
}else if (level == 3){
    perfect_guess_score = 20
}else{
    perfect_guess_score = 0
}
let incorrect_penalty = 1
let possible_points = perfect_guess_score
let currentRow = 1
let currentTile = 1
let isGameOver = false
let hintTile = 0

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
        const letter = test_answer_key[index][i]
        tile.textContent = letter
        guessRows[index][i] = letter
        tile.setAttribute('data', letter)
    }
}
addStartingWord(0)
addStartingWord(5)

// Add key listener to page
document.addEventListener('keydown', function (e) {
    if(!isGameOver){
        if ((e.key).match('^[a-z]{1}$')) {
            addLetter(e.key.toUpperCase())
        }
        if((e.key).match('^Backspace{1}$')){
            addLetter(e.key)
        }
        if((e.key).match('^Enter{1}$')){
            if(modalDisplay.style.display == 'block'){
                closeModalFunction()
            }else{
                checkRow()
            }
        }
    }
})

// Add letter to tile layout
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

// Delete letter from tile layout
const deleteLetter = () => {
    if (currentTile > hintTile) {
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

// Flip tiles
const flipTile = () => {
    const rowTiles = document.querySelector('#guessRow-' + currentRow).childNodes
    rowTiles.forEach((tile, index) => {
        setTimeout(() => {
            tile.classList.add('flip')
        }, 50 * index)
    })
}

// Shake tiles when answer entered
const shakeTile = () => {
    const rowTiles = document.querySelector('#guessRow-' + currentRow).childNodes
    rowTiles.forEach((tile) => {
        tile.classList.add('shake')
        setTimeout(() => {
            tile.classList.remove('shake')
        }, 50)
    })    
}

// Check button
checkButton.addEventListener('click', () => handleCheckClick())
const handleCheckClick = () => {
    if(!isGameOver){
        checkRow()
    }
}

// Checks current row
const checkRow = () => {
    const guess = guessRows[currentRow].join('')
    if(guess != test_answer_key[currentRow]){
        if(possible_points != 0){
            possible_points -= incorrect_penalty
        }
        shakeTile()
        if(hintTile == test_answer_key[currentRow].length - 1){
            isGameOver = true
            score += possible_points
            possible_points = perfect_guess_score 
            updateScore(score) 
            createModalMessage('Game over! Your score is: ' + score)
            createModalButtons('PLAY AGAIN', newGame)  
            modalDisplay.style.display = 'block'   
            return          
        }else{
            createModalMessage('Nice try! The next letter of the word is "' + test_answer_key[currentRow][hintTile] +'"')
            createModalButtons('OK', closeModalFunction)
            modalDisplay.style.display = 'block'
            addHint(currentRow, hintTile)
            clearRow(currentRow)
            currentTile = hintTile
        }
    }else{
        flipTile()
        if(currentRow == 4){
            isGameOver = true
            score += possible_points
            possible_points = perfect_guess_score 
            updateScore(score) 
            createModalMessage('Nice work! Your score is: ' + score)
            createModalButtons('PLAY AGAIN', newGame)  
            modalDisplay.style.display = 'block'       
            return
        }else{
            currentRow++
            currentTile = 1
            score += possible_points
            hintTile = 0
            createModalMessage('Nice job! The next word starts with "' + test_answer_key[currentRow][hintTile] +'"')
            createModalButtons('OK', closeModalFunction)
            modalDisplay.style.display = 'block'
            addHint(currentRow, hintTile)
            updateScore(score)
        }
    }
}

// Add hint
const addHint = (row, tile) => {
    letter = test_answer_key[row][tile]
    const hTile = document.getElementById('guessRow-' + row + '-tile-' + tile)
    hTile.textContent = letter
    guessRows[row][tile] = letter
    hTile.setAttribute('data', letter)
    hintTile++
}
addHint(1, 0)

// Clear button
clearButton.addEventListener('click', () => handleClearClick())
const handleClearClick = () => {
    if(!isGameOver){
        clearRow(currentRow)
    }
}

// Clear row
const clearRow = (index) => {
    for (let i = hintTile; i < guessRows[index].length; i++){
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
const createModalMessage = (modalMessage) => {
    const modalElement = document.createElement('p')
    modalElement.textContent = modalMessage
    modalElement.setAttribute('id', 'modal-message')
    modalContent.append(modalElement)
}

// Modal button
const createModalButtons = (buttonContent, buttonFunction) => {
    const modalButton = document.createElement('button')
    modalButton.onclick = buttonFunction
    modalButton.innerHTML = buttonContent
    modalButton.classList.add('modal-button')
    modalButton.setAttribute('id', 'modal-button')
    modalContent.append(modalButton)
}

// Close modal
const closeModalFunction = () => {
    const modalMessage = document.getElementById('modal-message')
    const modalButton = document.getElementById('modal-button')
    modalMessage.remove()
    modalButton.remove()
    modalDisplay.style.display = 'none'
}

// Start a new game
// Send out score and chain
// Get new chain
// Clear out tiles
const newGame = () => {
    closeModalFunction()
    clearTiles()
}

// Clear tiles
const clearTiles = () => {
    hintTile = 0
    for (let i = 0; i < guessRows.length; i++){
        clearRow(i)
    }
}
