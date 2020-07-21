from .Go import Go


class TwoPlayer(Go):
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
