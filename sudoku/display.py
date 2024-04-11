from IPython.display import display, HTML, Javascript, IFrame
import base64


def display_sudoku_old(grid):
    # Table start with overall styling
    table_html = '<table cellspacing="0" cellpadding="5" style="border-collapse: collapse; border: 2px solid black;">'

    for i, row in enumerate(grid):
        table_html += '<tr style="background-color: white;">'
        for j, cell in enumerate(row):
            # Determine cell borders
            border_styles = []
            if j == 2:
                border_styles.append("border-left: 2px solid black;")
            if i == 2:
                border_styles.append("border-top: 2px solid black;")

            if not border_styles:  # if there are no thick borders, set the thin ones to gray
                cell_style = "border: 1px solid gray; "
            else:
                cell_style = "border: 1px solid gray; " + ' '.join(border_styles)

            table_html += '<td style="{}">{}</td>'.format(cell_style, cell if cell != 0 else '&nbsp;')
        table_html += '</tr>'
    table_html += '</table>'
    display(HTML(table_html))

def display_sudoku(grid):
    # Table start with overall styling
    table_html = '<table cellspacing="0" cellpadding="5" style="border-collapse: collapse; border: 2px solid black;">'

    for i, row in enumerate(grid):
        table_html += '<tr style="background-color: white;">'
        for j, cell in enumerate(row):
            # Determine cell borders
            border_styles = []
            if j == 2:
                border_styles.append("border-left: 2px solid black;")
            if i == 2:
                border_styles.append("border-top: 2px solid black;")

            # Set cell style including size, alignment, and borders
            if not border_styles:  # if there are no thick borders, set the thin ones to gray
                cell_style = "width: 15px; height: 15px; text-align: center; border: 1px solid gray; font-size: 18px;"
            else:
                cell_style = "width: 15px; height: 15px; text-align: center; border: 1px solid gray; font-size: 18px; " + ' '.join(border_styles)

            table_html += '<td style="{}">{}</td>'.format(cell_style, cell if cell != 0 else '&nbsp;')
        table_html += '</tr>'
    table_html += '</table>'
    display(HTML(table_html))

def display_sudoku_comparison(grid1, grid2):
    # Ensure both grids are of the same size
    assert len(grid1) == len(grid2) and len(grid1[0]) == len(grid2[0]), "Grid sizes do not match"

    # Table start with overall styling
    table_html = '<table cellspacing="0" cellpadding="5" style="border-collapse: collapse;  border: 2px solid black;">'

    for i, row in enumerate(grid1):
        table_html += '<tr style="background-color: white;">'
        for j, cell in enumerate(row):
            # Determine cell borders
            border_styles = []
            if j == 2:
                border_styles.append("border-left: 2px solid black;")
            if i == 2:
                border_styles.append("border-top: 2px solid black;")

            # Check for differences and set font color if different
            font_color = "color: red;" if grid1[i][j] != grid2[i][j] else ""

            if not border_styles:  # if there are no thick borders, set the thin ones to gray
                cell_style = "border: 1px solid gray; " + font_color
            else:
                cell_style = "border: 1px solid gray; " + ' '.join(border_styles) + font_color

            #cell_style = "border: 1px solid black; " + ' '.join(border_styles) + font_color

            table_html += '<td style="{}">{}</td>'.format(cell_style, cell if cell != 0 else '&nbsp;')
        table_html += '</tr>'
    table_html += '</table>'
    display(HTML(table_html))

def get_sudoku_comparison(grid1, grid2):
    # Ensure both grids are of the same size
    assert len(grid1) == len(grid2) and len(grid1[0]) == len(grid2[0]), "Grid sizes do not match"

    # Table start with overall styling
    table_html = '<table cellspacing="0" cellpadding="5" style="border-collapse: collapse;  border: 2px solid black;">'

    for i, row in enumerate(grid1):
        table_html += '<tr style="background-color: white;">'
        for j, cell in enumerate(row):
            # Determine cell borders
            border_styles = []
            if j == 2:
                border_styles.append("border-left: 2px solid black;")
            if i == 2:
                border_styles.append("border-top: 2px solid black;")

            # Check for differences and set font color if different
            font_color = "color: red;" if grid1[i][j] != grid2[i][j] else ""

            if not border_styles:  # if there are no thick borders, set the thin ones to gray
                cell_style = "width: 15px; height: 15px; text-align: center; border: 1px solid gray; " + font_color
            else:
                cell_style = "width: 15px; height: 15px; text-align: center; border: 1px solid gray; " + ' '.join(border_styles) + font_color

            #cell_style = "border: 1px solid black; " + ' '.join(border_styles) + font_color

            table_html += '<td style="{}">{}</td>'.format(cell_style, cell if cell != 0 else '&nbsp;')
        table_html += '</tr>'
    table_html += '</table>'
    return table_html

# Your HTML, CSS, and JavaScript content for the grid and detail display area
header_content = """
<!DOCTYPE html>
<html>
<head>
<style>
/* CSS for grid layout */
#grid {
    display: grid;
    grid-template-columns: repeat(10, 30px);
    gap: 2px;
}
.cell {
    width: 30px;
    height: 30px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}
.correct { background: lightgreen; }
.incorrect { background: tomato; }
.unprocessed { background: lightgray; }
#detail {
    margin-left: 20px;
}
</style>
</head>
<body>
<div style="display: flex;">
    <div id="grid">
"""

def display_outcomes(outcomes):
    content = header_content
    # Arrays to store HTML and reasoning for each cell
    grid_htmls = []
    reasonings = []
    headlines = []
    total_correct = 0
    for i in range(100):
        icon = '&#183;'
        cell_class = 'unprocessed'
        grid_html = ''
        reasoning = ''
        headline = ''
        if i < len(outcomes):
            outcome = outcomes[i]
            if outcome['result'] == 'correct':
                icon = '&#10003;'
                cell_class = 'correct'
                headline = '<span style="color: lightgreen;">Correct &#10003;</span>'
                total_correct += 1
            elif outcome['result'] == 'incorrect':
                icon = '&#10007;'
                cell_class = 'incorrect'
                headline = '<span style="color: tomato;">Incorrect &#10007;</span>'
            grid_html = get_sudoku_comparison(outcome['proposed'], outcome['puzzle'])
            reasoning = outcome['reasoning']

        grid_htmls.append(grid_html)
        reasonings.append(reasoning)
        headlines.append(headline)
        content += f'<div id="cell{i}" class="cell {cell_class}">{icon}</div>'

    content += """
        </div>
        <div id="detail">
            <p>Click on an example to see details here.</p>
        </div>
    </div>
    <div><h3> Correct: """ + str(total_correct) + """ out of """ + str(len(outcomes))+ """ </h3></div>
    <script>
    function showDetail(cellId, outcome) {
        console.log('Detail shown for cell ' + cellId + ' with outcome ' + outcome);
        var detailDiv = document.getElementById('detail');
        var gridHtmls = """ + str(grid_htmls) + """;
        var reasonings = """ + str(reasonings) + """;
        var headlines = """ + str(headlines) + """;
        detailDiv.innerHTML = '<h3>Example ' + cellId + ': ' + headlines[cellId] + '</h3>' +
            '<div style="display: block;">' +
                '<div style="display: inline-block; vertical-align: top;">' +
                    // Assuming you want to keep this empty div
                '</div>' +
                '<div style="display: inline-block; vertical-align: top;">' +
                    '<div style="float: right; padding: 10px; margin-right: 20px;">' +
                        gridHtmls[cellId] + // gridHtmls content
                    '</div>' +
                    '<div>' +
                        reasonings[cellId] + // reasonings content
                    '</div>' +
                '</div>' +
            '</div>';
    }
    """

    # Adding event listeners
    for i in range(100):
        result_ = outcomes[i]['result'] if i < len(outcomes) else 'unprocessed'
        content += f'document.getElementById("cell{i}").addEventListener("click", function() {{ showDetail({i}, "{result_}"); }});'

    content += """
    </script>
    </body>
    </html>
    """

    # Encode the content
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # Create the iframe element with the encoded content as the src
    iframe_html = f'<iframe src="data:text/html;base64,{encoded_content}" width="800" height="800"></iframe>'

    # Display the iframe in the Jupyter Notebook
    display(IFrame(src="data:text/html;base64," + encoded_content, width=800, height=400))

    # Ensure display_sudoku_comparison is defined and returns HTML content


def display_outcomes_2(outcomes):
    content = header_content
    # Arrays to store HTML and reasoning for each cell
    grid_htmls = []
    reasonings = []

    for i in range(100):
        icon = '&#183;'
        cell_class = 'unprocessed'
        grid_html = ''
        reasoning = ''
        if i < len(outcomes):
            outcome = outcomes[i]
            if outcome['result'] == 'correct':
                icon = '&#10003;'
                cell_class = 'correct'
            elif outcome['result'] == 'incorrect':
                icon = '&#10007;'
                cell_class = 'incorrect'
            grid_html = get_sudoku_comparison(outcome['proposed'], outcome['puzzle'])
            reasoning = outcome['reasoning']

        grid_htmls.append(grid_html)
        reasonings.append(reasoning)
        content += f'<div id="cell{i}" class="cell {cell_class}">{icon}</div>'

    content += """
        </div>
        <div id="detail">
            <p>Click on an example to see details here.</p>
        </div>
    </div>
    <script>
    var lastSelectedCellId = window.lastSelectedCellId || null;

    function showDetail(cellId, outcome) {
        console.log('Detail shown for cell ' + cellId + ' with outcome ' + outcome);
        var detailDiv = document.getElementById('detail');
        var gridHtmls = """ + str(grid_htmls) + """;
        var reasonings = """ + str(reasonings) + """;
        detailDiv.innerHTML = '<h3>Example ' + cellId + ':</h3>' +
            '<div style="display: flex;">' +
                '<div style="flex: 1;">' + '</div>' +
                '<div style="flex: 2;">' + gridHtmls[cellId] + '</div>' +
                '<div style="flex: 3;">' + reasonings[cellId] + '</div>' +
            '</div>';
        window.lastSelectedCellId = cellId;
    }

    function restoreSelection() {
        if (lastSelectedCellId !== null) {
            showDetail(lastSelectedCellId, document.getElementById('cell' + lastSelectedCellId).className.split(' ')[1]);
        }
    }
    """

    # Adding event listeners
    for i in range(100):
        result_ = outcomes[i]['result'] if i < len(outcomes) else 'unprocessed'
        content += f'document.getElementById("cell{i}").addEventListener("click", function() {{ showDetail({i}, "{result_}"); }});'

    content += """
    window.onload = restoreSelection;
    </script>
    </body>
    </html>
    """

    # Encode the content
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # Create the iframe element with the encoded content as the src
    iframe_html = f'<iframe src="data:text/html;base64,{encoded_content}" width="800" height="800"></iframe>'

    # Display the iframe in the Jupyter Notebook
    display(IFrame(src="data:text/html;base64," + encoded_content, width=800, height=400))



def display_outcomes_3(outcomes):
    content = header_content
    # Arrays to store HTML and reasoning for each cell
    grid_htmls = []
    reasonings = []

    for i in range(100):
        icon = '&#183;'
        cell_class = 'unprocessed'
        grid_html = ''
        reasoning = ''
        if i < len(outcomes):
            outcome = outcomes[i]
            if outcome['result'] == 'correct':
                icon = '&#10003;'
                cell_class = 'correct'
            elif outcome['result'] == 'incorrect':
                icon = '&#10007;'
                cell_class = 'incorrect'
            grid_html = get_sudoku_comparison(outcome['proposed'], outcome['puzzle'])
            reasoning = outcome['reasoning']

        grid_htmls.append(grid_html)
        reasonings.append(reasoning)
        content += f'<div id="cell{i}" class="cell {cell_class}">{icon}</div>'

    content += """
        </div>
        <div id="detail">
            <p>Click on an example to see details here.</p>
        </div>
    </div>
    <script>

    function showDetail(cellId, outcome) {
        console.log('Detail shown for cell ' + cellId + ' with outcome ' + outcome);
        var detailDiv = document.getElementById('detail');
        var gridHtmls = """ + str(grid_htmls) + """;
        var reasonings = """ + str(reasonings) + """;
        detailDiv.innerHTML = '<h3>Example ' + cellId + ':</h3>' +
            '<div style="display: flex;">' +
                '<div style="flex: 1;">' + '</div>' +
                '<div style="flex: 2;">' + gridHtmls[cellId] + '</div>' +
                '<div style="flex: 3;">' + reasonings[cellId] + '</div>' +
            '</div>';
         window.localStorage.setItem('lastSelectedCellId', cellId.toString());
    }

    function restoreSelection() {
        var lastSelectedCellId = window.localStorage.getItem('lastSelectedCellId');
        if (lastSelectedCellId !== null) {
            lastSelectedCellId = parseInt(lastSelectedCellId, 10); // Convert back to integer
            showDetail(lastSelectedCellId, document.getElementById('cell' + lastSelectedCellId).className.split(' ')[1]);
        }
    }
    """

    # Adding event listeners
    for i in range(100):
        result_ = outcomes[i]['result'] if i < len(outcomes) else 'unprocessed'
        content += f'document.getElementById("cell{i}").addEventListener("click", function() {{ showDetail({i}, "{result_}"); }});'

    content += """
    window.onload = restoreSelection;
    </script>
    </body>
    </html>
    """

    # Encode the content
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # Create the iframe element with the encoded content as the src
    iframe_html = f'<iframe src="data:text/html;base64,{encoded_content}" width="800" height="800"></iframe>'

    # Display the iframe in the Jupyter Notebook
    display(IFrame(src="data:text/html;base64," + encoded_content, width=800, height=400))



def display_games(games):
    header_content = """
<!DOCTYPE html>
<html>
<head>
<style>
/* CSS for grid and cell layout */

#fullcontainer {
    display: flex;
    flex-direction: row;
    gap: 5px; 
}

#grid {
    display: flex;
    flex-direction: column;
    gap: 5px; /* Space between each game's row */
    border: 1px solid black;
    min-height: 200px;
    padding: 10px;
}
.cell {
    width: 20px;
    height: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-right: 2px; /* Space between cells */
}
.correct { background: lightgreen; }
.incorrect { background: tomato; }
.startcell { background: #D5D5D5; }
.solved { background: #ffd700; }
.game-row {
    display: flex; /* Align cells in a row */
    width: 270px;
}
#detail {

    margin-top: 0px; /* Space above the detail section */

}

.puzzle-analysis{
  display: flex;
  align-items: flex-start;
  
  margin-left: 20 px;
}

.puzzle-table {
  float: right;
  margin-right: 20px;
}

.reasoning-container {
  flex: 1;
  
}
</style>
</head>
<body>
<div id="fullcontainer">
<div id="grid">
"""

    content = header_content  # Initializes the HTML structure
    step_htmls = []
    reasonings = []
    puzzles = []  # To hold the puzzle states for each step

    for game_id, game in enumerate(games):
        game_html = '<div class="game-row">'
        prev_step_0 = None
    
        for step_id, step in enumerate(game['move']):
            icon = '&#10003;' if step[2] == 'correct' else '&#10007;' if step[2] == 'incorrect' else '&#10004;' 
            cell_class = 'correct' if step[2] == 'correct' else 'incorrect' if step[2] == 'incorrect' else 'solved'
    
            if step_id == 0:
                # For the first step, repeat step[0] as the final parameter - possible symbols: &#9632;
                game_html += f'<div id="cell{game_id}_{step_id}" class="cell startcell" onclick="updateGameStepDetails({game_id}, {step_id}, `{step[1]}`, {step[0]}, {step[0]})">&#9654;</div>'
            elif step[2] == 'solved':
                # If solved, show solved cell
                game_html += f'<div id="cell{game_id}_{step_id}" class="cell solved" onclick="updateGameStepDetails({game_id}, {step_id}, `{step[1]}`, {step[0]}, {prev_step_0})">{icon}</div>'
            else:
                # For subsequent steps, use the previous step[0] as the final parameter
                game_html += f'<div id="cell{game_id}_{step_id}" class="cell {cell_class}" onclick="updateGameStepDetails({game_id}, {step_id}, `{step[1]}`, {step[0]}, {prev_step_0})">{step_id}</div>'
    
            puzzles.append(step[0])
            reasonings.append(step[1])
            prev_step_0 = step[0]  # Store the current step[0] for the next iteration
    
        game_html += '</div>'  # Close game row
        content += game_html

    content += """
</div>
<div id="detail">
    <p>Click on a step to see details here.</p>
</div>
</div>
<script>
function updateGameStepDetails(gameNumber, stepNumber, reasoning, puzzle, prev_puzzle) {
    var detailDiv = document.getElementById('detail');

    // Clear previous content
    detailDiv.innerHTML = '';

    // Check for an existing comparison and remove it
    while (detailDiv.firstChild) {
      detailDiv.removeChild(container.firstChild);
    }

    // Create the header for game and step numbers
    var header = document.createElement('h3');
    header.textContent = 'Game ' + gameNumber + ' - Step ' + stepNumber;
    header.style.marginLeft = '10px';
    detailDiv.appendChild(header);

    var puzzleAnalysis = document.createElement('div');
    puzzleAnalysis.className = 'puzzle-analysis';
    puzzleAnalysis.id = 'puzzle-analysis'; // Assign an ID to the puzzleAnalysis element
    puzzleAnalysis.style.marginLeft = '20px';
    detailDiv.appendChild(puzzleAnalysis);



    // Create and append the reasoning container and text
    var reasoningContainer = document.createElement('div');
    reasoningContainer.className = 'reasoning-container';
    reasoningContainer.textContent = reasoning;
    
    //var reasoningText = document.createElement('p');
    //reasoningText.textContent = reasoning;
    //reasoningContainer.appendChild(reasoningText);

    // Append the reasoning next to the puzzle
    puzzleAnalysis.appendChild(reasoningContainer);
    
    // Draw the puzzle
    // drawPuzzle(puzzle, 'detail'); // This will append the puzzle to the detail div directly
    display_sudoku_comparison(puzzle, prev_puzzle, 'puzzle-analysis') //'detail'

}

function display_sudoku_comparison(grid1, grid2, containerId) {
  // Ensure both grids are of the same size
  if (grid1.length !== grid2.length || grid1[0].length !== grid2[0].length) {
    throw new Error("Grid sizes do not match");
  }

  var container = document.getElementById(containerId);
  //container.style.display = 'flex';
  //container.style.flexDirection = 'column'; 
  //container.style.alignItems = 'center';

  // Create the table for the comparison
  var table = document.createElement('table');
  table.className = 'puzzle-table';
  table.style.borderCollapse = 'collapse';
  table.style.margin = '10px';
  table.style.border = '2px solid black';
  table.cellSpacing = '0';
  table.cellPadding = '5';

  grid1.forEach(function(rowData, rowIndex) {
    var row = document.createElement('tr');
    row.style.backgroundColor = 'white';

    rowData.forEach(function(cellData, cellIndex) {
      var cell = document.createElement('td');

      // Determine cell borders
      var borderStyles = [];
      if (cellIndex === 2) borderStyles.push("border-left: 2px solid black;");
      if (rowIndex === 2) borderStyles.push("border-top: 2px solid black;");

      // Check for differences and set font color if different
      var fontColor = (grid1[rowIndex][cellIndex] !== grid2[rowIndex][cellIndex]) ? "color: red;" : "";

      if (borderStyles.length === 0) {
        // If there are no thick borders, set the thin ones to gray
        cell.style.border = "1px solid gray";
        cell.style.cssText += fontColor;
      } else {
        cell.style.border = "1px solid gray";
        cell.style.cssText += borderStyles.join(' ') + fontColor;
      }
      cell.style.height = '15px';
      cell.style.width = '15px';
      cell.style.textAlign = 'center';
      cell.style.verticalAlign = 'middle';
      cell.style.padding = '5px';

      // Display the cell value or a non-breaking space if 0
      cell.innerHTML = (cellData !== 0) ? cellData : '&nbsp;';

      row.appendChild(cell);
    });

    table.appendChild(row);
  });



  // Append the new comparison table to the container
  container.appendChild(table);
}

</script>
</body>
</html>
"""

    # Encode the content
    import base64
    from IPython.display import display, IFrame
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # Create and display the iframe
    display(IFrame(src="data:text/html;base64," + encoded_content, width=800, height=600))