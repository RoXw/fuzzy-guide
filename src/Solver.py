from collections import namedtuple
import heapq
import time
from enum import Enum

from Board import Board


class DistanceMetric(Enum):
    MANHATTAN = 0
    HAMMING = 1


class SearchNode:
    def __init__(
        self, priority: int, board: Board,  moves: int, searchNode=None
    ) -> None:
        self.board = board
        self.priority = priority
        self.parent = searchNode
        self.moves = moves

    def __lt__(self, other):
        return self.priority < other.priority

# SearchNode = namedtuple("SearchNode", ["priority", "board", "moves", "parent"])


class Solver:
    def __init__(self, tiles: list[list], distance: str = "Manhattan") -> None:
        self.board = Board(tiles)
        self.stack = []
        startTime = time.time()
        resultNode, self.moves, self.exploredNodes = self.solve(self.board, distance, 0)
        print(f"Total time taken: {round(time.time() - startTime, 4)} seconds")

        while resultNode != None:
            self.stack.append(resultNode.board)
            resultNode = resultNode.parent

    @staticmethod
    def solve(board, distance, moves):
        twinBoard = board.twin()
        exploredNodes = 0
        minPQ = []

        heapq.heappush(minPQ, SearchNode(board.manhattan(), board, 0, None))
        minPQTwin = []
        heapq.heappush(minPQTwin, SearchNode(twinBoard.manhattan(), twinBoard, 0, None))

        while True:
            currSearchNode = heapq.heappop(minPQ)
            currTwinSearchNode = heapq.heappop(minPQTwin)
            exploredNodes += 1
            if currSearchNode.board.isGoal():
                return (currSearchNode, moves, exploredNodes)

            if currTwinSearchNode.board.isGoal():
                return (None, -1, exploredNodes)

            for neighbor in currSearchNode.board.neighbors():
                if (currSearchNode.parent == None) or (
                    currSearchNode.parent.board != neighbor
                ):
                    heapq.heappush(
                        minPQ,
                        SearchNode(
                            neighbor.manhattan() + currSearchNode.moves + 1,
                            neighbor,
                            currSearchNode.moves + 1,
                            currSearchNode,
                        ),
                    )

            for neighbor in currTwinSearchNode.board.neighbors():
                if (currTwinSearchNode.parent == None) or (
                    currTwinSearchNode.parent.board != neighbor
                ):
                    heapq.heappush(
                        minPQTwin,
                        SearchNode(
                            neighbor.manhattan() + currTwinSearchNode.moves + 1,
                            neighbor,
                            currTwinSearchNode.moves + 1,
                            currTwinSearchNode,
                        ),
                    )

    def isSolvable(self):
        return self.moves > -1

    def TotalMoves(self):
        return self.moves

    def solution(self):
        return self.stack[::-1]
