
from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer
# The above import statement assumes that the player.py file is in the same directory as this file.
import time

# This is the main class for the Tic Tac Toe game


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # A list to hold the board state
        self.current_winner = None  # Keep track of the winner!

    def print_board(self):
        # We will print the board after every move
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # We will print the board after every move
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)]
                        for j in range(3)]
        for row in number_board:
            # print('| ' + ' | '.join(row) + ' |')
            # Using join to create a string representation of the row
            # and then printing it with pipe symbols
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # List comprehension to find empty spots
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        # Check if there are any empty squares left
        return ' ' in self.board

    def num_empty_squares(self):
        # Count the number of empty squares
        return self.board.count(' ')

    def make_move(self, square, letter):
        # Assign the letter to the square on the board
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check the row, column, and diagonals for a win
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Check the column
        col_ind = square % 3
        # Create a list comprehension to get the column
        # The column is formed by taking every third element starting from col_ind
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals

        if square % 2 == 0:
            # The first diagonal (top-left to bottom-right)
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            # The second diagonal (top-right to bottom-left)
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False  # If no win condition is met, return False


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'  # Starting letter
    # Loop until the game is over
    while game.empty_squares():
        # Get the current player's move
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # Make the move on the board
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')  # Empty line for better readability
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # Return the winner's letter
            # after a move, alternate the letter
            letter = 'O' if letter == 'X' else 'X'

        # tiny break to make the game more readable
        if print_game:
            time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')  # If no empty squares left and no winner


if __name__ == '__main__':
    x_wins = 0
    o_wins = 0
    ties = 0
    for _ in range(1000):  # Play 1000 games
        x_player = RandomComputerPlayer('X')
        o_player = GeniusComputerPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)

        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1
    print(
        f'After 1000 games: X wins: {x_wins}, O wins: {o_wins}, Ties: {ties}')
