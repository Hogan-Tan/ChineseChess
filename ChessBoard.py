from chessman.Bing import *
from chessman.Shuai import *
from chessman.Pao import *
from chessman.Shi import *
from chessman.Xiang import *
from chessman.Ma import *
from chessman.Che import *
# import logging
#
# logging.basicConfig(filename='output.txt', level=logging.INFO, format='%(asctime)s %(message)s')


class ChessBoard:
    pieces = dict()
    pieces[4, 0] = Shuai(True)
    pieces[0, 3] = Bing(True)
    pieces[2, 3] = Bing(True)
    pieces[4, 3] = Bing(True)
    pieces[6, 3] = Bing(True)
    pieces[8, 3] = Bing(True)
    pieces[1,2] = Pao(True)
    pieces[7,2] = Pao(True)
    pieces[3,0] = Shi(True)
    pieces[5,0] = Shi(True)
    pieces[2,0] = Xiang(True)
    pieces[6,0] = Xiang(True)
    pieces[1, 0] = Ma(True)
    pieces[7, 0] = Ma(True)
    pieces[0, 0] = Che(True)
    pieces[8, 0] = Che(True)
    pieces[4, 9] = Shuai(False)
    pieces[0, 6] = Bing(False)
    pieces[2, 6] = Bing(False)
    pieces[4, 6] = Bing(False)
    pieces[6, 6] = Bing(False)
    pieces[8, 6] = Bing(False)
    pieces[1,7] = Pao(False)
    pieces[7,7] = Pao(False)
    pieces[3,9] = Shi(False)
    pieces[5,9] = Shi(False)
    pieces[2,9] = Xiang(False)
    pieces[6,9] = Xiang(False)
    pieces[1, 9] = Ma(False)
    pieces[7, 9] = Ma(False)
    pieces[0, 9] = Che(False)
    pieces[8, 9] = Che(False)

    selected_piece = None

    def __init__(self):
        pass

    @staticmethod
    def get_move_locs(board, x, y):
        moves = []
        for xn in range(9):
            for yn in range(10):
                if board.pieces.get((xn, yn)) == board.selected_piece:
                    moves.append((xn, yn))
                elif board.can_move(x, y, xn-x, yn-y):
                    moves.append((xn, yn))
                else:
                    continue
        return moves

    def can_move(self, x, y, dx, dy):
        nx, ny = x + dx, y + dy
        if isinstance(self.pieces[x, y], Shuai):
            if (self.pieces[x, y].is_red and 3 <= nx <= 5 and 0 <= ny <= 2) or (
                    (not self.pieces[x, y].is_red) and 3 <= nx <= 5 and 7 <= ny <= 9
            ):
                if abs(dx) + abs(dy) == 1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True
            return False

        elif isinstance(self.pieces[x, y], Bing):
            if self.pieces[x, y].is_red and y < 5:
                if dx == 0 and dy == 1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True
            elif not self.pieces[x, y].is_red and y >= 5:
                if dx == 0 and dy == -1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True
            elif self.pieces[x, y].is_red and y >= 5:
                if abs(dx) + abs(dy) == 1 and dy != -1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True
            elif not self.pieces[x, y].is_red and y < 5:
                if abs(dx) + abs(dy) == 1 and dy != 1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True
            return False

        elif isinstance(self.pieces[x, y], Pao):
            if dx == 0 or dy == 0:
                cnt = self.pieces[x, y].count_pieces(self, x, y, dx, dy)
                if self.pieces.get((nx, ny)):
                    if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                        if cnt == 1:
                            return True
                else:
                    if cnt == 0:
                        return True

        elif isinstance(self.pieces[x, y], Shi):
            if self.pieces[x, y].is_red and 3 <= nx <= 5 and 0 <= ny <= 2:
                if abs(dx) == abs(dy) == 1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True
            elif not self.pieces[x, y].is_red and 3 <= nx <= 5 and 7 <= ny <= 9:
                if abs(dx) == abs(dy) == 1:
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True

        elif isinstance(self.pieces[x, y], Xiang):
            if self.pieces[x, y].is_red and ny < 5:
                if abs(dx) == abs(dy) == 2:
                    if not self.pieces.get((x + dx / 2, y + dy / 2)):
                        if self.pieces.get((nx, ny)):
                            if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                                return True
                        else:
                            return True
            elif not self.pieces[x, y].is_red and ny > 4:
                if abs(dx) == abs(dy) == 2:
                    if not self.pieces.get((x + dx / 2, y + dy / 2)):
                        if self.pieces.get((nx, ny)):
                            if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                                return True
                        else:
                            return True

        elif isinstance(self.pieces[x, y], Ma):
            if abs(dx) + abs(dy) == 3 and abs(dx) != 0 and abs(dy) != 0:
                if not self.pieces.get((x if abs(dx) == 1 else x + dx / 2, y if abs(dy) == 1 else y + (dy / 2))):
                    if self.pieces.get((nx, ny)):
                        if self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                            return True
                    else:
                        return True

        elif isinstance(self.pieces[x, y], Che):
            if dx == 0 or dy == 0:
                cnt = self.pieces[x, y].count_pieces(self, x, y, dx, dy)
                if self.pieces.get((nx, ny)):
                    if cnt == 0 and self.pieces.get((nx, ny)).is_red != self.pieces[x, y].is_red:
                        return True
                elif cnt == 0:
                    return True
        return False

    def move(self, x, y, dx, dy):
        nx, ny = x + dx, y + dy
        if (nx, ny) in self.pieces:
            self.remove(nx, ny)

        # 获取要移动的棋子
        piece = self.pieces[(x, y)]

        # 删除旧的位置
        del self.pieces[(x, y)]

        # 添加新的位置
        self.pieces[(nx, ny)] = piece

    def remove(self, x, y):
        del self.pieces[x, y]

    def select(self, x, y, player_is_red):
        if not self.selected_piece:
            if (x, y) in self.pieces and self.pieces[x, y].is_red == player_is_red:
                self.pieces[x, y].selected = True
                self.selected_piece = (x, y), self.pieces[x, y]
            return False

        if not (x, y) in self.pieces:  # 若x,y没有棋子
            if self.selected_piece:
                (ox, oy), piece = self.selected_piece
                if self.can_move(ox, oy, x-ox, y-oy):
                    self.move(ox, oy, x-ox, y-oy)
                    self.pieces[x,y].selected = False
                    self.selected_piece = None
                    return True
            return False

        if self.pieces[x, y].selected:
            return False

        if self.pieces[x, y].is_red != player_is_red:
            (ox, oy), piece = self.selected_piece
            if self.can_move(ox, oy, x-ox, y-oy):
                self.move(ox, oy, x-ox, y-oy)
                self.pieces[x, y].selected = False
                self.selected_piece = None
                return True
            return False
        for key in self.pieces.keys():
            self.pieces[key].selected = False
        self.pieces[x, y].selected = True
        self.selected_piece = (x, y), self.pieces[x, y]
        return False
