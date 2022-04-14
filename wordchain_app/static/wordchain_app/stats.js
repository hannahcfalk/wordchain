// Get HTML elements
const gameDisplay = document.querySelector(".completed-games")
//const scriptSource = document.getElementById("all-game-stats-js")
//const gameList = JSON.parse(scriptSource.getAttribute("data-scores"))
const gameList = JSON.parse(document.getElementById("all-scores").innerHTML)
const downloadButton = document.getElementById("download-button")
const downloadContainer = document.querySelector(".download-container")

// Create table
function createTable (){
    var tableElement = document.createElement('table')
    var tableHeadings = document.createElement('tr')

    var firstWordHeading = document.createElement('td')
    tableHeadings.appendChild(document.createTextNode("First Word"))
    tableHeadings.appendChild(firstWordHeading)
    var firstWordHeading = document.createElement('td')
    tableHeadings.appendChild(document.createTextNode("Sixth Word"))
    tableHeadings.appendChild(firstWordHeading)
    var firstWordHeading = document.createElement('td')
    tableHeadings.appendChild(document.createTextNode("Score"))
    tableHeadings.appendChild(firstWordHeading)
    tableElement.append(tableHeadings)

    for (let i = 0; i < gameList.length; i++) {
        var tableRow = document.createElement('tr')
        for (let j = 0; j < gameList[i].length; j++){
            var tableData = document.createElement('td')
            //document.createTextNode(gameList[i][j])
            tableRow.appendChild(document.createTextNode(gameList[i][j]))
            tableRow.appendChild(tableData)
        }
        tableElement.appendChild(tableRow)
    }
    //tableElement.appendChild(tableBody)
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
