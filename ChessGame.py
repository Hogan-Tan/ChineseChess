from ChessBoard import *
from ChessView import ChessView
import time
# from MCTS.ChineseChess_MCTS_debug import GameState, MCTS
# from MCTS.ChineseChess_MCTS_v1_0 import GameState, MCTS
from MCTS.ChineseChess_MCTS_v2_0 import GameState, MCTS


def real_coord(x):
    if x <= 50:
        return 0
    else:
        return int((((x-30)/40)*2+1)/2)  # 四舍五入


def board_coord(x):
    return 30 + 40*x


class ChessGame:

    def __init__(self):
        self.board = ChessBoard()
        self.player_is_red = True
        self.view = ChessView(self)
        self.view.showMsg("Red")
        self.view.draw_board(self.board)

    def start(self):
        self.view.start()

    def callback(self, event):
        rx, ry = real_coord(event.x), real_coord(event.y)
        if self.board.select(rx, ry, self.player_is_red):
            self.player_is_red = not self.player_is_red
            self.view.showMsg("Red" if self.player_is_red else "Green")
        self.view.draw_board(self.board)

    def press_a(self, event):  # 运行MCTS.ChineseChess_MCTS_debug.py，蒙特卡洛树算法自动下棋
    #     initial_state = GameState(self.board, self.player_is_red)
    #     mcts = MCTS(initial_state, iterations=50)
    #     mcts.search()
    #     best_move = mcts.get_best_move()
    #     print("Best move:", best_move)
    #     initial_state.execute_move(best_move)
    #     self.board = initial_state.board
    #     self.player_is_red = not self.player_is_redb
    #     self.view.draw_board(self.board)
        pass

    def press_b(self, event):  # 运行MCTS.ChineseChess_MCTS_v1.0.py，蒙特卡洛树算法自动下棋
        start_time_main = time.time()
        initial_state = GameState(self.board, self.player_is_red)
        mcts = MCTS(initial_state, iterations=100)
        mcts.search()
        best_move = mcts.get_best_move()
        print('Best move:', best_move)
        initial_state.execute_move(best_move)

        end_time_main = time.time()
        elapsed_time_main = end_time_main - start_time_main
        print(f'Main module execution time: {elapsed_time_main:.6f} seconds')
        self.board = initial_state.board
        self.player_is_red = not self.player_is_red
        self.view.draw_board(self.board)

    def press_c(self, event):  # 运行MCTS.ChineseChess_MCTS_v2.0.py。先扩展，再剪枝，再用蒙特卡洛树算法自动下棋
        initial_state = GameState(self.board, self.player_is_red)
        mcts = MCTS(initial_state)
        mcts.all_expend()
        self.board = initial_state.board
        self.player_is_red = not self.player_is_red
        self.view.draw_board(self.board)


game = ChessGame()
game.start()


