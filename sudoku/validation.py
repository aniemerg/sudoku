import ast
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage  
  


def is_single_cell_proposed(puzzle, proposed):
    """
    Returns True if only one cell is proposed as a solution.
    """
    differences = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != proposed[i][j]:
                differences += 1
    return differences == 1

def is_proposed_solution_valid(puzzle, solution, proposed):
    """
    Verifies if the proposed solution is valid for a single cell.
    """
    if not is_single_cell_proposed(puzzle, proposed):
        return False

    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != proposed[i][j] and proposed[i][j] != solution[i][j]:
                return False

    return True


def is_analysis_a_valid_puzzle(analysis):
    try:
        puzzle = ast.literal_eval(analysis)
        if not isinstance(puzzle, list):
            print("Not list")
            return False
        if len(puzzle) != 4:
            print("Wrong num of rows")
            return False
        for row in puzzle:
            if len(row) != 4:
                print("Wrong num of columns")
                return False
            for item in row:
                if item not in {0,1,2,3,4}:
                    print("Not numerical elements")
                    return False
    except:
        # raise
        return False
    return True




# This function is far from perfect and in at least one run GPT-4 marked 12 answers wrong that were right. 
def analysis_to_puzzle_solution(GPT4model, ft_puzzle, analysis):    
       
    # Messages for the puzzle update task
    fhm = '''We are working on the following sudoku puzzle (each sub-list represents a row):
    [[0, 1, 2, 0], [3, 2, 1, 0], [1, 0, 0, 0], [0, 4, 3, 0]]

    Below is an analysis that describes the solution to a cell, can you updated the puzzle with the solved cell? 
    Please don't explain, just output the updated puzzle. 

    Analysis: Looking at the second row, we see that numbers 3, 2, and 1 are already present in that row. 
    That leaves only 4 to complete the row. Therefore, row 3, column 4 is a 4. 
    '''

    am1 = "[[0, 1, 2, 0], [3, 2, 1, 4], [1, 0, 0, 0], [0, 4, 3, 0]]"

    fhm2 = '''Ok, now can you do this puzzle and analysis?
    Puzzle:
    [[3, 1, 2, 0], [0, 2, 3, 0], [0, 0, 0, 2], [2, 4, 1, 0]]

    Analysis: Let's look at the cell at row 3 and column 2. Row 3 has the number 2. Column 2 has the numbers 1, 2, 
    and 4. Region 3 has the numbers 2 and 4. Thus the cell cannot be: 1, 2 and 4. The solution to the cell is 3.
    '''

    am2 = "[[3, 1, 2, 0], [0, 2, 3, 0], [0, 3, 0, 2], [2, 4, 1, 0]]"

    fhm3 = '''Ok, now can you do this puzzle and analysis?
    Puzzle:
    {}

    Analysis: {}
    '''  
    if is_analysis_a_valid_puzzle(analysis):
        return ast.literal_eval(analysis)
    
    # Now update the puzzle/put it in computer readable form
    prompt = fhm3.format(ft_puzzle, analysis)
    update_message = GPT4model.predict_messages([HumanMessage(content=fhm),
                                  AIMessage(content=am1),
                                  HumanMessage(content=fhm2),
                                  AIMessage(content=am2),
                                  HumanMessage(content=prompt)
                                 ])  
    try:
        proposed = ast.literal_eval(update_message.content)
          
    except:
        raise Exception(f"Failed decoding following message to solution: {update_message.content}")
    return proposed