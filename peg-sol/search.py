import sys
import time

from board import Board
from priorityQueue import priority_queue
from board import Spot as heuristics

class BFS:
    def __init__(self, start):
        self.start = start
        self.visited = []
        self.nodes_visited = 0
        self.space = 0

    def search(self):
        queue = [(self.start, [])]

        while queue:
            self.space = max(self.space, len(queue))
            (state, path) = queue.pop(0)
            self.nodes_visited += 1

            for move, board in state.successors():
                if board in self.visited:
                    continue
                else:
                    self.visited += [board]

                if board.is_goal():
                    yield path + [move]
                else:
                    queue.append((board, path + [move]))


class AStar:
    def __init__(self, start, heuristic):
        self.start = start
        self.heuristic = heuristic
        self.visited = []
        self.nodes_visited = 0
        self.space = 0

    def search(self):
        pq = priority_queue(self.heuristic)
        pq.put((self.start, []))
        while not pq.empty():
            self.space = max(self.space, len(pq))

            state, path = pq.get()
            self.nodes_visited += 1

            if state.is_goal():
                yield path
            for move, board in state.successors():
                if board in self.visited:
                    continue
                else:
                    self.visited += [board]

                pq.put((board, path + [move]))


def main():
    start_board = Board.board_from_file(sys.argv[1])
    method = sys.argv[2]
    heuristic = heuristics.manhattan_distance

    start = time.time()
    if method == 'bfs':
        seeker = BFS(start_board)
        try:
            path = next(seeker.search())
        except StopIteration:
            path = None

    elif method == 'astar':
        seeker = AStar(start_board, heuristic)
        try:
            path = next(seeker.search())
        except StopIteration:
            path = None

    else:
        print('Invalid...')
        return

    end = time.time()

    print("-" * 30)
    print('Graph Search Method: ', sys.argv[2] if len(sys.argv) > 2 else '')
    print('Input File:', sys.argv[1])
    print('Moves:')

    if path:
        for step in path:
            print(step[0], '-->', step[1])
    else:
        print("No solution found!")

    print('Time: {0:.4f} seconds'.format(end - start))
    print('Nodes Visited:', seeker.nodes_visited)
    print('Space: {} nodes'.format(seeker.space))

    if hasattr(seeker, 'visited'):
        print('Visited Size:', len(seeker.visited))

    print("-" * 30)


if __name__ == '__main__':
    main()
