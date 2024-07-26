from numba import njit
from numba.typed import List


class Board:
    def __init__(self, tiles) -> None:
        self.n = len(tiles)
        self.tiles = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                self.tiles[i][j] = tiles[i][j]

    def __str__(self) -> str:
        return "\n".join([" ".join([str(x) for x in row]) for row in self.tiles])

    def __eq__(self, value: object) -> bool:
        if not value:
            return False
        if not isinstance(value, Board):
            return False
        if self.n != value.n:
            return False
        for i in range(self.n):
            for j in range(self.n):
                if self.tiles[i][j] != value.tiles[i][j]:
                    return False
        return True

    def __lt__(self, other) -> bool:
        dist1 = self.manhattan()
        dist2 = other.manhattan()
        return dist1 < dist2

    def isGoal(self):
        pos = 1
        for i in range(self.n):
            for j in range(self.n):
                if self.tiles[i][j] != pos % (self.n * self.n):
                    return False
                pos += 1
        return True

    def hamming(self):
        distance = 0
        pos = 1
        for i in range(self.n):
            for j in range(self.n):
                if self.tiles[i][j] != pos:
                    distance += 1
                pos += 1
                pos = pos % (self.n * self.n)
        return distance

    def manhattan(self):
        distance = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.tiles[i][j] > 0:
                    x = (self.tiles[i][j] - 1) // self.n
                    y = (self.tiles[i][j] - 1) % self.n
                    distance += abs(x - i) + abs(y - j)
        return distance

    def twin(self):
        i, j = 0, 0
        if self.tiles[i][j] == 0:
            j += 1

        if j == self.n - 1:
            directions = [[0, -1], [-1, 0]]
        else:
            directions = [[0, 1], [1, 0]]
        i_, j_ = i, j
        for d in directions:
            i_ = i + d[0]
            j_ = j + d[1]

            if (
                i_ >= 0
                and j_ >= 0
                and i_ < self.n
                and j_ < self.n
                and self.tiles[i_][j_] > 0
            ):
                break

        twinTiles = [[0] * self.n for _ in range(self.n)]
        for x in range(self.n):
            for y in range(self.n):
                twinTiles[x][y] = self.tiles[x][y]

        temp = twinTiles[i][j]
        twinTiles[i][j] = twinTiles[i_][j_]
        twinTiles[i_][j_] = temp

        return Board(twinTiles)

    def neighbors(self):
        neigh = []
        directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]

        for zeroIx in range(self.n):
            for zeroIy in range(self.n):
                if self.tiles[zeroIx][zeroIy] == 0:
                    break
            if self.tiles[zeroIx][zeroIy] == 0:
                break

        tiles_copy = [row.copy() for row in self.tiles]

        for d in directions:
            newIx, newIy = zeroIx + d[0], zeroIy + d[1]
            if 0 <= newIx < self.n and 0 <= newIy < self.n:
                tiles_copy[zeroIx][zeroIy], tiles_copy[newIx][newIy] = (
                    self.tiles[newIx][newIy],
                    0,
                )
                neigh.append(Board(tiles_copy))
                tiles_copy[zeroIx][zeroIy], tiles_copy[newIx][newIy] = (
                    0,
                    self.tiles[newIx][newIy],
                )
        return neigh

    def pprint(self):
        for x in range(self.n):
            print(" | ".join(str(v) for v in self.tiles[x]))
        print("--" * self.n)
