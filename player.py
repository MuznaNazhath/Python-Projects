import math
import random


class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

        # we want all players to get their next move given a game

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # Randomly choose a valid move
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            # Check if the input is a digit and within the valid range
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True  # if the square is valid
            except ValueError:
                print('Invalid square. Try again.')

        return val  # Return the valid move as an integer


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # Use the minimax algorithm to find the best move
        if len(game.available_moves()) == 9:
            # Randomly choose a corner
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # The maximizer, aka your player
        other_player = 'O' if player == 'X' else 'X'  # The other player

        # First, we want to check if the previous move is a winner
        if state.current_winner == other_player:
            # We should return the score for the previous move
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}

        elif not state.empty_squares():
            # No empty squares left, it's a tie
            return {'position': None, 'score': 0}

        if player == max_player:
            # Start with the worst score for maximizer
            best = {'position': None, 'score': -math.inf}

        else:
            # Start with the worst score for minimizer
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():  # Loop through all possible moves
            # Make a move on the board
            state.make_move(possible_move, player)
            # Recursively call minimax for the next player
            sim_score = self.minimax(state, other_player)

            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            # Assign the position to the score
            sim_score['position'] = possible_move

            # Update the best score based on the player
            # If the player is the maximizer, we want to maximize the score
            # If the player is the minimizer, we want to minimize the score
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score  # Update the best score for maximizer
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score  # Update the best score for minimizer

        return best  # Return the best score and position
        # This will be used to find the best move for the player
