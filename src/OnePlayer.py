from .Go import Go
import random


class OnePlayer(Go):
    counter = 0

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def oval_selected(self, event):
        if self.is_done(self.board):
            self.log.set("game over")
            return
        index = event.widget.find_closest(event.x, event.y)[0] - 334
        x = int(index/Go.SIZE)
        y = int(index % Go.SIZE)
        self.log.set("")
        if not self.player_move_and_set(x, y, self.get_player(), self.board, self.prev_board):
            return
        self.end_turn()
        # self.random_play(self.get_player())
        x, y, r = self.minimax(
            Go.WHITE, self.board, self.prev_board, 1, float('-inf'), float('+inf'), True)
        self.player_move_and_set(x, y,
                                 self.get_player(), self.board, self.prev_board)
        self.end_turn()

    def random_play(self, player):
        list = self.valids(player, self.board)
        selected = random.choice(list)
        self.player_move_and_set(selected[0], selected[1],
                                 self.get_player(), self.board, self.prev_board)
        self.set_stone_on_gui(self.board)
        self.end_turn()

    def minimax(self, player, board, prev_board, level, alpha, beta, max_player):
        temp_board = {}
        temp_prev = {}
        oppo = -1 * player
        list = self.valids(player, board)
        if level == 0 or self.is_done(board) or len(list) == 0:
            return 0, 0, self.evaluation(board, player if max_player else -1 * player)
        if max_player:
            max_eval = float('-inf')
            for move in list:
                OnePlayer.counter += 1
                self.copy(board, temp_board)
                self.copy(prev_board, temp_prev)
                self.player_move(move[0], move[1], player,
                                 temp_board, temp_prev)
                evalu = self.minimax(
                    oppo, temp_board, temp_prev, level-1, alpha, beta, False)[2]
                if max_eval < evalu:
                    max_eval = evalu
                    best = move
                alpha = max(alpha, evalu)
                if beta <= alpha:
                    break
            return best[0], best[1], max_eval
        else:
            min_eval = float('inf')
            for move in list:
                OnePlayer.counter += 1
                self.copy(board, temp_board)
                self.copy(prev_board, temp_prev)
                self.player_move(move[0], move[1], player,
                                 temp_board, temp_prev)
                evalu = self.minimax(
                    oppo, temp_board, temp_prev, level-1, alpha, beta, True)[2]
                if min_eval > evalu:
                    min_eval = evalu
                    best = move
                beta = min(beta, evalu)
                if beta <= alpha:
                    break
            return best[0], best[1], min_eval

    def evaluation(self, board, player):
        evalu = 0
        weight = [
            [0, 8, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 8, 0],
            [8, 8, 7, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 7, 8, 8],
            [7, 7, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 7, 7],
            [6, 6, 6, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 6, 6, 6],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [6, 6, 6, 9, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 6, 6, 6],
            [7, 7, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 7, 7],
            [8, 8, 7, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 7, 8, 8],
            [0, 8, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 7, 8, 0]
        ]
        count = 0
        for i in range(Go.SIZE):
            for j in range(Go.SIZE):
                if board[i, j] == player:
                    count += 1
                    evalu += weight[i][j]
                if board[i, j] == -1 * player:
                    count -= 1
        return evalu + 10 * count
