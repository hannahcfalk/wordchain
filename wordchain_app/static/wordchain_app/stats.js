// Get HTML elements
const gameDisplay = document.querySelector(".completed-games")
const downloadContainer = document.querySelector(".download-container")
const downloadButton = document.getElementById("download-button")
const gameList = JSON.parse(document.getElementById("all-scores").innerHTML)

// Create table
function createTable (){
    if(gameList.length == 0){
        var no_scores = document.createElement('h4')
        no_scores.innerHTML = 'No Scores!'
        gameDisplay.append(no_scores)
        return
    }

    var tableElement = document.createElement('table')
    var tableHeadings = document.createElement('tr')

    var firstWordHeading = document.createElement('td')
    tableHeadings.appendChild(document.createTextNode("First Word"))
    tableHeadings.appendChild(firstWordHeading)

    var sixthWordHeading = document.createElement('td')
    tableHeadings.appendChild(document.createTextNode("Sixth Word"))
    tableHeadings.appendChild(sixthWordHeading)

    var scoreHeading = document.createElement('td')
    tableHeadings.appendChild(document.createTextNode("Score"))
    tableHeadings.appendChild(scoreHeading)
    tableElement.append(tableHeadings)

    for (let i = 0; i < gameList.length; i++) {
        var tableRow = document.createElement('tr')
        for (let j = 0; j < gameList[i].length; j++){
            var tableData = document.createElement('td')
            tableRow.appendChild(document.createTextNode(gameList[i][j]))
            tableRow.appendChild(tableData)
        }
        tableElement.appendChild(tableRow)
    }
    gameDisplay.appendChild(tableElement)
}
createTable()

// Download function
function download(filename, text){
    const element = document.createElement('a')
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    downloadContainer.append(element);
    element.click();
    downloadContainer.removeChild(element);
}

// Add download button
if (downloadButton && downloadContainer){
    downloadButton.addEventListener('click', function(){
        var text = document.getElementById("download-content").innerHTML
        var filename = 'stats.json'
        download(filename, text)
    }, false)
}
