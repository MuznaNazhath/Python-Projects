def find_next_empty(puzzle):
    # find the next row, col on the puzzle that is not filled yet
    # return a tuple (row, col) or (None, None) if there is none
    for r in range(9):
        for c in range(9):  # iterate through each column
            if puzzle[r][c] == -1:  # -1 means empty cell
                return r, c  # return the coordinates of the empty cell
    return None, None  # if no empty cell is found


def is_valid(puzzle, guess, row, col):
    # check if the guess is valid in the given row, column, and 3x3 box
    # return True if valid, False otherwise
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    # check the column
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # check if the guess is in the 3x3 box
    # we can find the top-left corner of the box using integer division
    # check the 3x3 box
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    # if we reach here, the guess is valid
    return True


def solve_sudoku(puzzle):
    # solve the sudoku puzzle using backtracking
    # step 1: find the next empty cell
    row, col = find_next_empty(puzzle)

    # step 1.1: if there is no empty cell, we are done
    if row is None:
        return True  # puzzle solved

    # step 2: try all numbers from 1 to 9
    for guess in range(1, 10):
        # step 3: check if the guess is valid
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess

            # step 4: recursively call the solve function
            if solve_sudoku(puzzle):
                return True

        # step 5: if the guess didn't work, reset the cell and try the next number
        # backtrack
        puzzle[row][col] = -1  # reset the cell to empty

    return False


if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(solve_sudoku(example_board))
    print(example_board)
