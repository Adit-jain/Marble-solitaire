import sys
from enum import IntEnum

import numpy as np


class Spot(IntEnum):
    PEG, FREE, OUT_OF_BOUNDS = range(3)

    def manhattan_distance(board):
        man = 0
        number_of_pegs = 0

        for r in range(board.size):
            for c in range(board.size):
                if board.board[r, c] == Spot.PEG:
                    number_of_pegs += 1
                    for rr in range(board.size):
                        for cc in range(board.size):
                            if board.board[rr, cc] == Spot.PEG:
                                man += abs(r - rr) + abs(c - cc)
        return man / (2 * number_of_pegs)


class Board:
    def __init__(self, board, directions):
        self.board = board
        self.size = board.shape[0]

        if type(directions) is str:
            if directions == 'all':
                self.directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
            elif directions == 'ortho':
                self.directions = ['n', 'e', 's', 'w']
            elif directions == 'swne':
                self.directions = ['n', 'ne', 'e', 's', 'sw', 'w']
        else:
            self.directions = directions

    @classmethod
    def board_from_file(cls, file_name):

        with open(file_name, 'r') as peg_file:
            directions, _, *matrix_lines = peg_file.readlines()

        matrix = np.array([[spot for spot in line.strip().split(' ')] for line in matrix_lines])

        board_matrix = np.zeros(matrix.shape, dtype=np.uint8)

        for r in range(matrix.shape[0]):
            for c in range(matrix.shape[1]):
                if matrix[r, c] == '*':
                    board_matrix[r, c] = int(Spot.PEG)
                elif matrix[r, c] == 'o':
                    board_matrix[r, c] = int(Spot.FREE)
                else:
                    board_matrix[r, c] = int(Spot.OUT_OF_BOUNDS)

        return Board(board=board_matrix, directions=directions.strip())

    @classmethod
    def board_from_board(cls, other):
        new_board = Board(np.copy(other.board), other.directions)
        return new_board

    def successors(self):
        moves = self.get_possible_moves()
        for move in moves:
            yield (move, self.make_move(*move))

    def check_peg(self, start_position, direction):
        return self._get_spot(start_position, direction) == Spot.PEG

    def is_goal(self):

        pegs = 0

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r, c] == Spot.PEG:
                    pegs += 1

                if pegs > 1:
                    return False
        return pegs == 1

    def get_possible_moves(self):

        for free_position in self._free_positions():
            yield from [(jump, free_position) for jump in self._possible_jumps_into_empty(free_position)]

    def make_move(self, source, destination):

        new_board = Board.board_from_board(self)

        # Calculate the coordinates of the pixel that is between the source and destination
        hop = tuple(np.divide(np.add(source, destination), (2, 2)))
        hop = tuple(map(int, hop))
        new_board.board[source] = Spot.FREE
        new_board.board[destination] = Spot.PEG
        new_board.board[hop] = Spot.FREE

        return new_board

    @staticmethod
    def _adjusts_coords_to_direction(start_position, direction):

        r, c = start_position
        r -= direction.count('n')
        r += direction.count('s')
        c += direction.count('e')
        c -= direction.count('w')

        return r, c

    def _possible_jumps_into_empty(self, empty_coord):

        for direction in self.directions:
            if self.check_peg(empty_coord, direction) and self.check_peg(empty_coord, direction * 2):
                yield self._adjusts_coords_to_direction(empty_coord, direction * 2)

    def _free_positions(self):

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r, c] == Spot.FREE:
                    yield (r, c)

    def _get_spot(self, start_position, direction):
        r, c = self._adjusts_coords_to_direction(start_position, direction)
        if self._out_of_bounds(r, c):
            return '.'

        return self.board[r, c]

    def _out_of_bounds(self, r, c):
        return min(r, c) < 0 or max(r, c) >= self.size

    def __eq__(self, other):
        return (self.board == other.board).all()

    def __str__(self):
        ret = '  '
        for i in range(self.size):
            ret += str(i) + ' '
        ret += '\n'

        for r in range(self.size):
            ret += str(r) + ' '
            for c in range(self.size):
                ret += '{} '.format(self.board[r, c])
            ret += '\n'
        return ret
