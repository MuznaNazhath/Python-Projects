
import random
import re
# lets create a board for a minesweeper game
# this is so that we can say "create a new board object " or "dig here" or "render the game for this  object"


class Board:
    def __init__(self, dim_size, num_bombs):
        # lets keep track of these parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # lets create the board
        # help function!
        self.board = self.make_new_board()  # plant the bombs
        self.assign_values_to_board()  # assign numbers to the board

        # initialize a set to keep track of which locations we've uncovered
        self.dug = set()  # locations that have been dug (i.e. revealed)

    def make_new_board(self):
        # helper function to create a new board
        # generate a random board with bombs planted
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            # randomly choose a location
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size  # integer division to get the row
            col = loc % self.dim_size  # modulus to get the column

            if board[row][col] == '*':  # if there's already a bomb here, skip
                continue
            board[row][col] = '*'  # plant a bomb
            bombs_planted += 1  # increment the number of bombs planted

        return board

    def assign_values_to_board(self):
        # helper function to assign numbers to the board
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue  # skip if there's a bomb here
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # helper function to count the number of bombs around a given cell
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at a specific location
        # return True if dug successfully, False if dug a bomb
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False  # dug a bomb
        elif self.board[row][col] > 0:
            return True

        # if we dug a cell with no neighboring bombs, we need to dig all neighboring cells
        for r in range(max(0, row - 1), min(self.dim_size-1, row + 1)+1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue  # already dug this cell
                self.dig(r, c)  # dig the neighboring cell

        return True

    def __str__(self):
        # string representation of the board
        # we will use this to print the board
        visible_board = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

                # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # create a new board
    board = Board(dim_size, num_bombs)

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)  # print the board
        # 0,4 or 0, 4 or 0,  4
        user_input = re.split(
            ', (\\s)*', input("Enter a row and column to dig (e.g., '0, 1'): "))  # 0, 4
        # get the row and column from user input
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid input. Please enter a valid row and column.")
            continue
        # valid input, dig the cell
        safe = board.dig(row, col)
        if not safe:
            print("You dug a bomb! Game over.")
            break

    if safe:
        print("Congratulations! You cleared the board.")
    else:
        print("Game Over:(")

    # let's reveal the board at the end
    board.dug = [(r, c) for r in range(board.dim_size)
                 for c in range(board.dim_size)]  # reveal all cells
    print(board)  # print the final board


if __name__ == "__main__":
    play()
