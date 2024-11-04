import random
import math
import time

from ChessBoard import ChessBoard
from chessman.Shuai import *


board = ChessBoard()


class GameState:
    def __init__(self, player_is_red=True):
        self.board = board
        self.board_pieces = self.board.pieces
        self.current_player = player_is_red

    # 检查游戏是否结束
    def is_end(self):
        # 检查是否有玩家获胜
        red_shuai_exists = any(isinstance(piece, Shuai) and piece.is_red for piece in self.board_pieces.values())
        black_shuai_exists = any(isinstance(piece, Shuai) and not piece.is_red for piece in self.board_pieces.values())

        if red_shuai_exists and not black_shuai_exists:
            return True, True
        elif not red_shuai_exists and black_shuai_exists:
            return True, False
        else:
            return False, '游戏继续'

    # 执行一个动作（移动棋子）
    def execute_move(self, move):
        x_f, y_f = move[0]
        x_t, y_t = move[1]
        self.board.select(x_f, y_f, self.current_player)
        # time.sleep(1)
        self.board.select(x_t, y_t, self.current_player)
        self.current_player = not self.current_player

    # 获取所有可能的合法动作
    def get_legal_moves(self, current_player):
        legal_moves = {}
        for locate, piece in self.board_pieces.items():
            if piece.is_red == current_player:
                legal_moves[locate] = piece.get_move_locs(self.board)
        return legal_moves


# 定义蒙特卡洛树搜索节点类
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}  # 存储子节点的字典，键为动作，值为MCTSNode对象
        self.visits = 0  # 该节点被访问的次数
        self.value = 0.0  # 该节点的累积价值（由模拟结果得出）

    def is_fully_expanded(self):
        # 检查子节点的数量是否等于当前状态下所有可能的合法动作的数量
        legal_moves_count = 0
        for legal_move_f, legal_move_t in self.state.get_legal_moves(self.state.current_player).items():
            legal_moves_count += len(legal_move_t)
        return len(self.children) == legal_moves_count
        # 这种方式假设了每次展开节点时，都会为当前状态下的所有合法动作创建子节点，不考虑当前是谁在行动（因为MCTS会交替选择动作）。这是井字游戏等回合制游戏中常见的做法。

    # 选择子节点，使用UCT公式
    def select_child(self, exploration_weight=math.sqrt(2)):  # 默认的探索权重为sqrt(2)
        if not self.children:
            return None
        selected_child = max(self.children.values(),
                             key=lambda c: (c.value / c.visits) + exploration_weight * math.sqrt(
                                 (2 * math.log(self.visits) / c.visits)))
        return selected_child

    # 展开节点（生成子节点）
    def expand(self):
        legal_moves = []
        for legal_moves_f, legal_moves_t in self.state.get_legal_moves(self.state.current_player).items():
            for legal_move_t in legal_moves_t:
                legal_moves.append((legal_moves_f, legal_move_t))
        if not legal_moves:
            return None
        # 过滤出未被扩展的合法移动
        unexpanded_moves = [move for move in legal_moves if move not in self.children]
        if not unexpanded_moves:
            return None  # 所有合法移动都已被扩展
        # 随机选择一个未被扩展的移动
        move = random.choice(unexpanded_moves)
        next_state = GameState(self.state.current_player)
        next_state.execute_move(move)
        child_node = MCTSNode(next_state, self)
        self.children[move] = child_node
        return child_node

    # 模拟游戏直到结束，并返回结果
    def simulate(self):
        visited_paths = set()  # 记录已访问的路径
        path = []  # 当前路径
        state = GameState(self.state.current_player)
        while True:
            end, winner = state.is_end()
            if end:
                if winner == self.state.current_player:
                    return 1.0
                else:
                    return 0.0
            re_count = 0
            re_count_quit = True
            while True:
                legal_moves = state.get_legal_moves(self.state.current_player)
                if not legal_moves:
                    return None  # 没有合法移动，返回默认值
                moves = []
                for legal_moves_f, legal_moves_t in legal_moves.items():
                    for legal_move_t in legal_moves_t:
                        moves.append((legal_moves_f, legal_move_t))
                move = random.choice(moves)  # 使用 random.choice 返回一个单一的移动
                path.append(move)
                path_tuple = tuple(path)
                if path_tuple not in visited_paths:
                    visited_paths.add(path_tuple)
                    break
                path.pop()  # 移除最后一个移动，重新选择
                re_count += 1
                if re_count > 100:  # 如果连续100次都遇到重复路径，则退出
                    re_count_quit = False
                    break
            if re_count_quit:
                if MCTSNode.loss_path(self) == 'loss':
                    return 'loss'
                else:
                    state.execute_move(move)
            else:
                return None

    def loss_path_result(self, move):
        state = GameState(self.state.current_player)
        state.current_player = not state.current_player
        state.execute_move(move)
        end, winner = state.is_end()
        if end:
            if winner:
                return 1
        return 0

    def loss_path(self):
        state = GameState(self.state.current_player)
        result_add = 0
        legal_moves = []
        for legal_moves_f, legal_moves_t in self.state.get_legal_moves(self.state.current_player).items():
            for legal_move_t in legal_moves_t:
                legal_moves.append((legal_moves_f, legal_move_t))
        for legal_move in legal_moves:
            result = MCTSNode.loss_path_result(self, legal_move)
            result_add += result
        if result_add != 0:
            return 'loss'


# 定义蒙特卡洛树搜索类
class MCTS:
    def __init__(self, initial_state, iterations=1000):
        self.root = MCTSNode(initial_state)
        self.iterations = iterations

        # 执行蒙特卡洛树搜索

    def search(self):
        for _ in range(self.iterations):
            node = self.root
            # 选择阶段
            while node.is_fully_expanded() and (node.select_child() is not None):
                node = node.select_child()
            # 展开阶段
            if node.is_fully_expanded() is False:
                node = node.expand()
            # 模拟阶段
            result_value = 0
            i = 0
            for i in range(self.iterations):
                result = node.simulate()
                if result is not None and result != 'loss':
                    result_value += result
                elif result == 'loss':
                    node.value = -100
                else:
                    break
            if i != 0:
                result_value = result_value/i+1
            # 回溯阶段
            while node is not None:
                node.visits += 1
                node.value += result_value
                node = node.parent

    # 获取最佳动作
    def get_best_move(self):
        best_move = max(self.root.children.values(), key=lambda c: (c.value / c.visits))
        return list(self.root.children.keys())[list(self.root.children.values()).index(best_move)]
