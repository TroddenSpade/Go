import tkinter as tk


class Go(tk.Frame):

    SIZE = 19
    WHITE = 1
    BLACK = -1
    WIDTH = 760
    CELL = 40
    BACKGROUND = '#d1a246'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.counter = 0
        self.config(bg=Go.BACKGROUND)
        self.__init_body__()
        self.__init_board__()
        self.point = {-1: 0, 1: 0}

    def __init_body__(self):
        self.turn = tk.StringVar()
        self.turn.set("Black's Turn")
        self.turn_label = tk.Label(self, textvariable=self.turn)
        self.turn_label.pack(side='top', fill='x')
        self.black_point = tk.StringVar()
        self.white_point = tk.StringVar()
        self.black_point.set("Black : 0")
        self.white_point.set("White : 0")
        self.black_point_label = tk.Label(self, textvariable=self.black_point)
        self.white_point_label = tk.Label(self, textvariable=self.white_point)
        self.black_point_label.pack(side='left', padx=(20, 20))
        self.white_point_label.pack(side='right', padx=(20, 20))
        self.log = tk.StringVar()
        self.log.set("")
        self.log_label = tk.Label(self, textvariable=self.log)
        self.log_label.pack(side='bottom', fill='x')
        self.canvas = tk.Canvas(self, width=Go.WIDTH, height=Go.WIDTH,
                                borderwidth=0, highlightthickness=0, bg=Go.BACKGROUND)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = Go.CELL
        self.cellheight = Go.CELL

    def __init_board__(self):
        self.board = {}
        self.oval = {}
        for column in range(Go.SIZE-1):
            for row in range(Go.SIZE-1):
                x1 = Go.CELL/2 + column * self.cellheight
                y1 = Go.CELL/2 + row * self.cellheight
                x2 = x1 + self.cellheight
                y2 = y1 + self.cellheight
                self.canvas.create_rectangle(x1, y1, x2, y2, tags="rect")
                if (row == 3 or row == 9 or row == 15) and (column == 3 or column == 9 or column == 15):
                    self.canvas.create_oval(
                        x1+2, y1+2, x1-2, y1-2, tags="oval", fill='black')
        for row in range(Go.SIZE):
            for column in range(Go.SIZE):
                self.board[row, column] = 0
                x1 = column * self.cellheight
                y1 = row * self.cellheight
                x2 = x1 + self.cellheight
                y2 = y1 + self.cellheight
                # if column < Go.SIZE-5 or row < Go.SIZE-5:
                #     self.board[row, column] = 1
                #     self.oval[row, column] = self.canvas.create_oval(
                #         x1+2, y1+2, x2-2, y2-2, tags="oval", fill='white', outline="")
                # else:
                self.oval[row, column] = self.canvas.create_oval(
                    x1+2, y1+2, x2-2, y2-2, tags="oval", fill='', outline="")
                self.canvas.tag_bind(
                    "oval", "<Button-1>", self.oval_selected)
        self.prev_board = {}
        self.copy(self.board, self.prev_board)

    def oval_selected(self, event):
        pass

    def end_turn(self):
        self.counter += 1
        self.white_point.set("White : " + str(self.point[Go.WHITE]))
        self.black_point.set("Black : " + str(self.point[Go.BLACK]))
        if self.get_player() == Go.WHITE:
            self.turn.set("White's turn")
        elif self.get_player() == Go.BLACK:
            self.turn.set("Black's turn")

    def player_move(self, x, y, player, board, prev_board):
        # temp = {}
        # self.copy(board, temp)
        cap_res = self.can_capture(x, y, player, board)
        if cap_res != False:
            for l in cap_res:
                board[l[0], l[1]] = 0
        board[x, y] = player
        # if self.counter > 1 and self.cmp_dic(board, prev_board):
        #     self.copy(temp, board)
        #     self.log.set("invalid move")
        #     return False
        # if self.counter > 1:
        #     self.copy(temp, prev_board)
        return True

    def player_move_and_set(self, x, y, player, board, prev_board):
        temp = {}
        self.copy(board, temp)
        if self.not_empty(x, y, board):
            self.log.set("invalid move")
            return False
        cap_res = self.can_capture(x, y, player, board)
        if cap_res != False:
            for l in cap_res:
                board[l[0], l[1]] = 0
        else:
            if self.has_liberty(x, y, player, board) != True:
                self.log.set("invalid move")
                return False
        board[x, y] = player
        if self.counter > 1 and self.cmp_dic(board, prev_board):
            self.copy(temp, board)
            self.log.set("invalid move")
            return False
        self.set_stone_on_gui(temp)
        if self.counter > 1:
            self.copy(temp, prev_board)
        return True

    def set_stone_on_gui(self, temp):
        for x in range(Go.SIZE):
            for y in range(Go.SIZE):
                if self.board[x, y] != temp[x, y]:
                    if self.board[x, y] == Go.WHITE:
                        fill = "white"
                    elif self.board[x, y] == Go.BLACK:
                        fill = "black"
                    else:
                        self.point[self.get_player()] += 1
                        fill = ""
                    self.canvas.itemconfig(self.oval[x, y], fill=fill)

    def can_capture(self, x, y, player, board):
        list = []
        board[x, y] = player
        oppo = -1 * player
        if 0 <= y-1 < Go.SIZE and board[x, y-1] == oppo:
            res = self.has_liberty(x, y-1, oppo, board)
            if res != True:
                list = list + res
        if 0 <= y+1 < Go.SIZE and board[x, y+1] == oppo:
            res = self.has_liberty(x, y+1, oppo, board)
            if res != True:
                list = list + res
        if 0 <= x-1 < Go.SIZE and board[x-1, y] == oppo:
            res = self.has_liberty(x-1, y, oppo, board)
            if res != True:
                list = list + res
        if 0 <= x+1 < Go.SIZE and board[x+1, y] == oppo:
            res = self.has_liberty(x+1, y, oppo, board)
            if res != True:
                list = list + res
        board[x, y] = 0
        if len(list) == 0:
            return False
        return list

    def is_done(self, board):
        for i in range(Go.SIZE):
            for j in range(Go.SIZE):
                if self.is_valid(i, j, self.get_player(), board):
                    return False
        return True

    def valids(self, player, board):
        list = []
        for i in range(Go.SIZE):
            for j in range(Go.SIZE):
                if self.is_valid(i, j, player, board):
                    list.append((i, j))
        return list

    def is_valid(self, x, y, player, board):
        if self.not_empty(x, y, board):
            return False
        if self.can_capture(x, y, player, board) != False:
            return True
        if self.has_liberty(x, y, player, board) != True:
            return False
        return True

    def has_liberty(self, x, y, player, board):
        '''
        if there is a liberty return True
        esle return all of the group
        '''
        state_board = {}
        for row in range(Go.SIZE):
            for column in range(Go.SIZE):
                state_board[row, column] = 0
        if self.liberty_recursion(x, y, state_board, board, player) == True:
            return True
        group = []
        for i in range(Go.SIZE):
            for j in range(Go.SIZE):
                if state_board[i, j] != 0:
                    group.append((i, j))
        return group

    def liberty_recursion(self, x, y, state_board, board, player):
        if (
            (0 <= y-1 < Go.SIZE and board[x, y-1] == 0 and state_board[x, y-1] == 0) or
            (0 <= y+1 < Go.SIZE and board[x, y+1] == 0 and state_board[x, y+1] == 0) or
            (0 <= x-1 < Go.SIZE and board[x-1, y] == 0 and state_board[x-1, y] == 0) or
            (0 <= x+1 < Go.SIZE and board[x+1, y]
             == 0 and state_board[x+1, y] == 0)
        ):
            return True
        state_board[x, y] = player
        if (
            (0 <= y-1 < Go.SIZE and state_board[x, y-1] == 0 and board[x, y-1] == player and self.liberty_recursion(x, y-1, state_board, board, player)) or
            (0 <= y+1 < Go.SIZE and state_board[x, y+1] == 0 and board[x, y+1] == player and self.liberty_recursion(x, y+1, state_board, board, player)) or
            (0 <= x-1 < Go.SIZE and state_board[x-1, y] == 0 and board[x-1, y] == player and self.liberty_recursion(x-1, y, state_board, board, player)) or
            (0 <= x+1 < Go.SIZE and state_board[x+1, y] == 0 and board[x+1, y]
             == player and self.liberty_recursion(x+1, y, state_board, board, player))
        ):
            return True
        return False

    def not_empty(self, x, y, board):
        return False if board[x, y] == 0 else True

    def get_player(self):
        if self.counter % 2 == 0:
            return Go.BLACK
        else:
            return Go.WHITE

    def cmp_dic(self, dic1, dic2):
        for l in dic1:
            if dic1[l] != dic2[l]:
                return False
        return True

    def copy(self, src, des):
        for l in src:
            des[l] = src[l]

    def print_board(self, board=None):
        if board is None:
            board = self.board
        print("  ", end=" ")
        for i in range(Go.SIZE):
            print('%2d' % i, end=" ")
        print()
        print("  ", end=" ")
        for i in range(Go.SIZE):
            print("--", end=" ")
        print()
        for row in range(Go.SIZE):
            print('%2d' % row, end="|")
            for column in range(Go.SIZE):
                print("", end=" ")
                print('%2d' % board[row, column], end="")
            print(" ")
