import time
import copy


def elem_iden(List):

    mt = set(List)
    if len(mt) == 1:
        winner = list(mt)[0]
        if winner != Game.Goal:
            return winner
        else:
            return False
    else:
        return False


class Game:

    NC_Row = 3
    NC_Columns = 3
    P_MIN = None
    P_MAX = None
    Goal = '#'

    def __init__(self, table=None):
        self.matrix = table or [Game.Goal]*(Game.NC_Columns * Game.NC_Row)

    def final(self):

        result = (elem_iden(self.matrix[0:3])
               or elem_iden(self.matrix[3:6])
               or elem_iden(self.matrix[6:9])
               or elem_iden(self.matrix[0:9:3])
               or elem_iden(self.matrix[1:9:3])
               or elem_iden(self.matrix[2:9:3])
               or elem_iden(self.matrix[0:9:4])
               or elem_iden(self.matrix[2:8:2]))

        if(result):
            return result
        elif Game.Goal not in self.matrix:
            return 'draw'
        else:
            return False

    def moves_game(self, player):

        l_moves = []

        for i in range(self.NC_Columns * self.NC_Row):
            if self.matrix[i] == "#":
                move = copy.deepcopy(self.matrix)
                move[i] = player
                l_moves.append(Game(move))

        return l_moves


    def line_Open(self, List, player):

        mt = set(List)

        if len(mt) <= 2:

            if mt <= {Game.Goal, player}:
                return 1
            else:
                return 0
        else:
            return 0

    def lines_open(self, player):
        return (self.line_Open(self.matrix[0:3], player)
                + self.line_Open(self.matrix[3:6], player)
                + self.line_Open(self.matrix[6:9], player)
                + self.line_Open(self.matrix[0:9:3], player)
                + self.line_Open(self.matrix[1:9:3], player)
                + self.line_Open(self.matrix[2:9:3], player)
                + self.line_Open(self.matrix[0:9:4], player)
                + self.line_Open(self.matrix[2:8:2], player))

    def estimates_score(self, depth):
        t_final = self.final()
        if t_final == Game.P_MAX:
            return (99 + depth)
        elif t_final == Game.P_MIN:
            return (-99 - depth)
        elif t_final == 'draw':
            return 0
        else:
            return self.lines_open(Game.P_MAX) - self.lines_open(Game.P_MIN)

    def __str__(self):
        row = (" ".join([str(x) for x in self.matrix[0:3]])+"\n" +
               " ".join([str(x) for x in self.matrix[3:6]])+"\n" +
               " ".join([str(x) for x in self.matrix[6:9]])+"\n")

        return row


class State:

    DEPTH_MAX = None

    def __init__(self, table_game, current_player, depth, parent=None, score=None):
        self.table_game = table_game
        self.current_player = current_player
        self.depth = depth
        self.score = score
        self.moves_possible = []
        self.state_selected = None

    def player_opposite(self):
        if self.current_player == Game.P_MIN:
            return Game.P_MAX
        else:
            return Game.P_MIN

    def moves_state(self):
        l_moves = self.table_game.moves_game(self.current_player)
        players_opposite = self.player_opposite()

        l_states_moves = [
            State(move, players_opposite, self.depth-1, parent=self) for move in l_moves]
        return l_states_moves

    def __str__(self):
        sir = str(self.table_game) + "(Current Player:" + self.current_player+")\n"
        return sir


""" Algorithm MiniMax """

def min_max(state):


    if state.depth == 0 or state.table_game.final():
        state.score = state.table_game.estimates_score(state.depth)
        return state

    state.moves_possible = state.moves_state()

    moves_score = [min_max(move) for move in state.moves_possible]

    if state.current_player == Game.P_MAX:
        state.state_selected = max(moves_score, key=lambda x: x.score)
    else:
        state.state_selected = min(moves_score, key=lambda x: x.score)

    state.score = state.state_selected.score
    return state



""" Algorithm Alpha-Beta """

def alpha_beta(alpha, beta, state):

    if state.depth == 0 or state.table_game.final():
        state.score = state.table_game.estimates_score(state.depth)
        return state

    if alpha >= beta:
        return state

    state.moves_possible = state.moves_state()

    if state.current_player == Game.P_MAX:
        score_current = float('-inf')


        for move in state.moves_possible:
            new_state = alpha_beta(alpha, beta, move)

            if score_current < new_state.score:
                state.state_selected = new_state
                score_current = new_state.score

            if alpha < new_state.score:
                alpha = new_state.score
                if alpha >= beta:
                    break

    elif state.current_player == Game.P_MIN:
        score_current = float('inf')

        for move in state.moves_possible:
            new_state = alpha_beta(alpha, beta, move)

            if score_current > new_state.score:
                state.state_selected = new_state
                score_current = new_state.score

            if beta > new_state.score:
                beta = new_state.score
                if alpha >= beta:
                    break


    state.score = state.state_selected.score

    return state


def display_if_final(state_current):
    final = state_current.table_game.final()
    if(final):
        if (final == "draw"):
            print("Draw!")
        else:
            print(final+" Won")

        return True

    return False


def main():

    answer_valid = False
    while not answer_valid:
        type_algoritm = input(
            "The algorithm used? (answer with 1 or 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
        if type_algoritm in ['1', '2']:
            answer_valid = True
        else:
            print("You did not choose the right option.")


    answer_valid = False
    while not answer_valid:
        n = input("Maximum shaft depth: ")
        if n.isdigit():
            State.DEPTH_MAX = int(n)
            answer_valid = True
        else:
            print("You must enter a non-zero natural number.")


    answer_valid = False
    while not answer_valid:
        Game.P_MIN = input("Do you want to play with x or o ? ").lower()
        if (Game.P_MIN in ['x', 'o']):
            answer_valid = True
        else:
            print("Answer must be x or o.")
    Game.P_MAX = 'o' if Game.P_MIN == 'x' else 'x'


    table_current = Game()
    print("Initial table")
    print(str(table_current))


    state_current = State(table_current, 'x', State.DEPTH_MAX)

    while True:
        if (state_current.current_player == Game.P_MIN):
            answer_valid = False
            while not answer_valid:
                try:
                    line = int(input("Row="))
                    column = int(input("Column="))

                    if (line in range(0, 3) and column in range(0, 3)):
                        if state_current.table_game.matrix[line*3+column] == Game.Goal:
                            answer_valid = True
                        else:
                            print("A symbol already exists in the required position.")
                    else:
                        print("Invalid row or column (must be one of the numbers 0,1,2).")

                except ValueError:
                    print("Row and column must be integers")


            state_current.table_game.matrix[line*3+column] = Game.P_MIN


            print("\nTable after moving player")
            print(str(state_current))


            if (display_if_final(state_current)):
                break

            state_current.current_player = state_current.player_opposite()


        else:

            t_before = int(round(time.time() * 1000))
            if type_algoritm == '1':
                state_updated = min_max(state_current)
            else:
                state_updated = alpha_beta(-500, 500, state_current)
            state_current.table_game = state_updated.state_selected.table_game
            print("Board after moving computer")
            print(str(state_current))

            t_after = int(round(time.time() * 1000))
            print("The computer takes time: " +
                  str(t_after-t_before)+" milliseconds.")

            if (display_if_final(state_current)):
                break

            state_current.current_player = state_current.player_opposite()


if __name__ == "__main__":
    main()
