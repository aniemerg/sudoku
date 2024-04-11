from copy import deepcopy
import random

def construct_puzzle_solution():
    while True:
        try:
            puzzle  = [[0]*4 for i in range(4)] # start with blank puzzle
            rows    = [set(range(1,5)) for i in range(4)] # set of available numbers for each row
            columns = [set(range(1,5)) for i in range(4)] # set of available numbers for each column
            squares = [set(range(1,5)) for i in range(4)] # set of available numbers for each square
            for i in range(4):
                for j in range(4):
                    # pick a number for cell (i,j) from the set of remaining available numbers
                    choices = rows[i].intersection(columns[j]).intersection(squares[(i//2)*2 + j//2])
                    choice  = random.choice(list(choices))

                    puzzle[i][j] = choice

                    rows[i].discard(choice)
                    columns[j].discard(choice)
                    squares[(i//2)*2 + j//2].discard(choice)

            # success! every cell is filled.
            return puzzle

        except IndexError:
            # if there is an IndexError, we have worked ourselves in a corner (we just start over)
            pass

def pluck(puzzle, n=0):
    history = []
    history.append(deepcopy(puzzle))
    puzzle_ = deepcopy(puzzle)
    # Can the cell (i,j) in the puzzle "puz" contain the number in cell "c"?
    def canBeA(puz, i, j, c):
        v = puz[c//4][c%4]
        if puz[i][j] == v: return True
        if puz[i][j] in range(1,5): return False

        for m in range(4): # test row, col, square
            # if not the cell itself, and the mth cell of the group contains the value v, then "no"
            if not (m==c//4 and j==c%4) and puz[m][j] == v: return False
            if not (i==c//4 and m==c%4) and puz[i][m] == v: return False
            if not ((i//2)*2 + m//2==c//4 and (j//2)*2 + m%2==c%4) and puz[(i//2)*2 + m//2][(j//2)*2 + m%2] == v:
                return False

        return True

    # Start with a set of all 16 cells, and tries to remove one (randomly) at a time
    # but not before checking that the cell can still be deduced from the remaining cells.
    cells     = set(range(16))
    cellsleft = cells.copy()
    while len(cells) > n and len(cellsleft):
        cell = random.choice(list(cellsleft)) # choose a cell from ones we haven't tried
        cellsleft.discard(cell) # record that we are trying this cell

        # row, col and square record whether another cell in those groups could also take
        # on the value we are trying to pluck. (If another cell can, then we can't use the
        # group to deduce this value.) If all three groups are True, then we cannot pluck
        # this cell and must try another one.
        row = col = square = False

        for i in range(4):
            if i != cell//4:
                if canBeA(puzzle_, i, cell%4, cell): row = True
            if i != cell%4:
                if canBeA(puzzle_, cell//4, i, cell): col = True
            if not (((cell//4)//2)*2 + i//2 == cell//4 and ((cell//4)%2)*2 + i%2 == cell%4):
                if canBeA(puzzle_, ((cell//4)//2)*2 + i//2, ((cell//4)%2)*2 + i%2, cell): square = True

        if row and col and square:
            continue # could not pluck this cell, try again.
        else:
            # this is a pluckable cell!
            puzzle_[cell//4][cell%4] = 0 # 0 denotes a blank cell
            cells.discard(cell) # remove from the set of visible cells (pluck it)
            history.append(deepcopy(puzzle_))

    # Return the modified puzzle and the number of cells left.
    return (puzzle_, len(cells), history)

def make_puzzle(solution):
    puzzle, _, _ = pluck(solution)
    return puzzle


def solve_sudoku(board):
    for row in range(4):
        for col in range(4):
            # Look for an empty cell
            if board[row][col] == 0:
                for num in range(1, 5):  # For 4x4 Sudoku, the numbers are 1 through 4
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def sudoku_solver(board):
    copy_ = deepcopy(board)
    solve_sudoku(copy_)
    return copy_


def get_constraints(grid, row, col):
    numbers = set(range(1, 5))

    # Determine region boundaries
    region_start_row = 2 * (row // 2)
    region_start_col = 2 * (col // 2)

    # Check for numbers in the same row, column, and region
    for i in range(4):
        if grid[row][i] in numbers:
            numbers.remove(grid[row][i])
        if grid[i][col] in numbers:
            numbers.remove(grid[i][col])
        if grid[region_start_row + i//2][region_start_col + i%2] in numbers:
            numbers.remove(grid[region_start_row + i//2][region_start_col + i%2])

    # Calculate and return the constraint value
    constraint_fraction = len(numbers) / 4
    return 1-constraint_fraction


def choose_solution_location(board):
    x_locs = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:
                constraint = get_constraints(board, i, j)
                if constraint >= 0.75:
                    x_locs.append((i,j))
    return random.choice(x_locs)

def weighted_random_choice(items):
    """
    Selects an item from the list with a probability that increases monotonically
    as the list progresses. The last item in the list has the highest likelihood of selection.
    """
    # Assigning weights that increase towards the end of the list
    weights = [i for i in range(1, len(items) + 1)]

    # Choosing an item based on the assigned weights
    return random.choices(items, weights=weights, k=1)[0]


def area_information(numbers, location, area):
    area_line = f"{area} {location} has no solved cells."
    if len(numbers) == 1:
        area_line = f"{area} {location} has one solved cell: {list(numbers)[0]}."
    elif len(numbers) == 2:
        area_line = f"{area} {location} has two solved cells: {list(numbers)[0]} and {list(numbers)[1]}."
    elif len(numbers) == 3:
        area_line = f"{area} {location} has three solved cells: {list(numbers)[0]}, {list(numbers)[1]} and {list(numbers)[2]}."
    return area_line


def format_non_zero_numbers(area, row_num, numbers):
    # Filter out non-zero numbers
    non_zeros = [n for n in numbers if n != 0]

    # Check if the filtered list is empty
    if not non_zeros:
        return ""

    # Format the non-zero numbers into the desired format
    if len(non_zeros) == 1:
        formatted = f"{area} {row_num+1} has the number {non_zeros[0]}."
    elif len(non_zeros) == 2:
        formatted = f"{area} {row_num+1} has the numbers {non_zeros[0]} and {non_zeros[1]}."
    else:
        all_except_last = ", ".join(map(str, non_zeros[:-1]))
        formatted = f"{area} {row_num+1} has the numbers {all_except_last}, and {non_zeros[-1]}."

    return formatted


def get_region(x, y):
    if x in [0, 1] and y in [0, 1]:
        return 1
    elif x in [2, 3] and y in [0, 1]:
        return 3
    elif x in [0, 1] and y in [2, 3]:
        return 2
    elif x in [2, 3] and y in [2, 3]:
        return 4
    else:
        return None  # For coordinates that don't fall into any region

def get_column(puzzle, number):
    return list((puzzle[0][number], puzzle[1][number], puzzle[2][number],  puzzle[3][number]))

def cells_for_region(region):
    """Returns the row and column range for the specified region."""
    if region == 1:
        return (0, 2), (0, 2)
    elif region == 2:
        return (0, 2), (2, 4)
    elif region == 3:
        return (2, 4), (0, 2)
    elif region == 4:
        return (2, 4), (2, 4)
    else:
        raise ValueError("Invalid region number")

def region_data(matrix, region):
    row_range, col_range = cells_for_region(region)

    # Extract non-zero values from the region
    non_zeros = [matrix[i][j] for i in range(row_range[0], row_range[1]) for j in range(col_range[0], col_range[1]) if matrix[i][j] != 0]

    # Format the output
    if not non_zeros:
        return f"Region {region} has no non-zero numbers."
    elif len(non_zeros) == 1:
        return f"Region {region} has the number {non_zeros[0]}."
    elif len(non_zeros) == 2:
        return f"Region {region} has the numbers {non_zeros[0]} and {non_zeros[1]}."
    else:
        all_except_last = ", ".join(map(str, non_zeros[:-1]))
        return f"Region {region} has the numbers {all_except_last}, and {non_zeros[-1]}."
