import copy


class LifeGame(object):
    """
    Class for Game life
    """
    EMPTY = 0
    ROCK = 1
    FISH = 2
    SHRIMP = 3
    MARK_FISH = -100
    MARK_SHRIMP = -101
    MARK_DIE_FISH = -1000
    MARK_CONTINUE_LIVE_FISH = -1001
    MARK_DIE_SHRIMP = -1002
    MARK_CONTINUE_LIVE_SHRIMP = -1003

    def __init__(self, board: list[list[int]]):
        self._board: list[list[int]] = board
        self._neighbours_board: list[list[int]] = copy.deepcopy(board)

    def get_next_generation(self) -> list[list[int]]:
        self._update_neighbours_board()
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j] == self.FISH:
                    if self._neighbours_board[i][j] == self.MARK_DIE_FISH:
                        self._board[i][j] = self.EMPTY
                    elif self._neighbours_board[i][j] == self.MARK_CONTINUE_LIVE_FISH:
                        self._board[i][j] = self.FISH
                elif self._board[i][j] == self.SHRIMP:
                    if self._neighbours_board[i][j] == self.MARK_DIE_SHRIMP:
                        self._board[i][j] = self.EMPTY
                    elif self._neighbours_board[i][j] == self.MARK_CONTINUE_LIVE_SHRIMP:
                        self._board[i][j] = self.SHRIMP
                elif self._board[i][j] == self.EMPTY:
                    if self._neighbours_board[i][j] == self.MARK_FISH:
                        self._board[i][j] = self.FISH
                    elif self._neighbours_board[i][j] == self.MARK_SHRIMP:
                        self._board[i][j] = self.SHRIMP
                    else:
                        self._board[i][j] = self.EMPTY
                else:
                    self._board[i][j] = self.ROCK

        return self._board

    def _update_neighbours_board(self) -> None:
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j] == LifeGame.FISH:
                    neighbours = self._count_neighbours(self.FISH, i, j)
                    if neighbours >= 4 or neighbours <= 1:
                        self._neighbours_board[i][j] = self.MARK_DIE_FISH
                    else:
                        self._neighbours_board[i][j] = self.MARK_CONTINUE_LIVE_FISH
                elif self._board[i][j] == LifeGame.SHRIMP:
                    neighbours = self._count_neighbours(self.SHRIMP, i, j)
                    if neighbours >= 4 or neighbours <= 1:
                        self._neighbours_board[i][j] = self.MARK_DIE_SHRIMP
                    else:
                        self._neighbours_board[i][j] = self.MARK_CONTINUE_LIVE_SHRIMP
                elif self._board[i][j] == LifeGame.EMPTY:
                    neighbours_fish = self._count_neighbours(self.FISH, i, j)
                    neighbours_shrimp = self._count_neighbours(self.SHRIMP, i, j)
                    if neighbours_fish == 3:
                        self._neighbours_board[i][j] = self.MARK_FISH
                    elif neighbours_shrimp == 3:
                        self._neighbours_board[i][j] = self.MARK_SHRIMP
                    else:
                        self._neighbours_board[i][j] = self.EMPTY
                else:
                    self._neighbours_board[i][j] = self.ROCK
                    continue

    def _count_neighbours(self, animal: int, index_i: int, index_j: int) -> int:
        neighbours = 0
        current_i = index_i - 1
        if current_i < 0:
            current_i = index_i
        current_j = index_j - 1
        if current_j < 0:
            current_j = index_j
        index_end_i = index_i + 1
        if index_end_i >= len(self._board):
            index_end_i = index_i
        index_end_j = index_j + 1
        if index_end_j >= len(self._board[0]):
            index_end_j = index_j
        remember_current_j = current_j
        while current_i <= index_end_i:
            while current_j <= index_end_j:
                if self._board[current_i][current_j] == animal:
                    if current_i == index_i and current_j == index_j:
                        current_j += 1
                        continue
                    neighbours += 1
                    current_j += 1
                else:
                    current_j += 1
            current_i += 1
            current_j = remember_current_j
        return neighbours


board = [
    [3], [3]
]
life_game = LifeGame(board)
print(life_game.get_next_generation())
