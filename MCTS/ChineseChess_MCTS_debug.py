import random
import math
import copy

from ChessBoard import ChessBoard
from chessman.Shuai import *


class GameState:

    def __init__(self, gamestate_board, player_is_red=True):
        self.board = gamestate_board
        self.current_player = player_is_red

    # 检查游戏是否结束
    def is_end(self):
        # 检查是否有玩家获胜
        red_shuai_exists = any(isinstance(piece, Shuai) and piece.is_red for piece in self.board.pieces.values())
        black_shuai_exists = any(isinstance(piece, Shuai) and not piece.is_red for piece in self.board.pieces.values())

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
        # print(self.board.pieces)
        # print(move)
        self.board.select(x_f, y_f, self.current_player)
        self.board.select(x_t, y_t, self.current_player)
        self.current_player = not self.current_player

    # 获取所有可能的合法动作
    def get_legal_moves(self, current_player):
        legal_moves = {}
        for locate, piece in self.board.pieces.items():
            if piece.is_red == current_player:
                self.board.select(locate[0], locate[1], current_player)
                get_moves = [x for x in piece.get_move_locs(self.board) if x != locate]
                if self.board.selected_piece is not None:
                    legal_moves[locate] = get_moves
                    self.board.select(locate[0], locate[1], current_player)  # 取消选择
                else:
                    self.board.select(locate[0], locate[1], current_player)
                    if self.board.selected_piece is not None:
                        legal_moves[locate] = get_moves
                        self.board.select(locate[0], locate[1], current_player)  # 取消选择
        return legal_moves

# 定义蒙特卡洛树搜索节点类
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = copy.deepcopy(state)  # 深拷贝当前状态，避免在模拟过程中修改原始状态
        self.parent = parent
        self.children = {}  # 存储子节点的字典，键为动作，值为MCTSNode对象
        self.visits = 0  # 该节点被访问的次数
        self.value = 0.0  # 该节点的累积价值（由模拟结果得出）

    def is_fully_expanded(self):
        legal_moves_count = sum(len(moves) for moves in self.state.get_legal_moves(self.state.current_player).values())
        return len(self.children) == legal_moves_count

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
        print('开始生成子节点')
        legal_moves = []
        expand_node = self
        expand_node.state.board.pieces = {k: v for k, v in self.state.board.pieces.items()}  # 深拷贝棋盘/
        for legal_moves_f, legal_moves_t in expand_node.state.get_legal_moves(expand_node.state.current_player).items():
            for legal_move_t in legal_moves_t:
                legal_moves.append((legal_moves_f, legal_move_t))  # legal_moves = [((x1f,y1f),(x1t,y1t)),...]
        if not legal_moves:
            return None
        # unexpanded_moves = [((x1f,y1f),(x1t,y1t)),...]
        unexpanded_moves = [move for move in legal_moves if move not in expand_node.children]
        if not unexpanded_moves:
            return None  # 所有合法移动都已被扩展
        move = random.choice(unexpanded_moves)  # move = ((xf,yf),(xt,yt))
        new_state = copy.deepcopy(expand_node.state)
        new_state.execute_move(move)
        # expand_node.state.execute_move(move)
        child_node = MCTSNode(new_state)
        expand_node.children[move] = child_node
        child_node.parent = expand_node
        return child_node

    # 模拟游戏直到结束，并返回结果
    def simulate(self):
        visited_paths = set()  # 记录已访问的路径
        sim_count_max = 300  # 最大模拟次数
        sim_count = 0
        path = []  # 当前路径
        # path_count_max = 1000  # 最大路径数量
        sim_node = self
        sim_node.state.board.pieces = {k: v for k, v in self.state.board.pieces.items()}  # 深拷贝棋盘/
        # sim_state = GameState(self.state.board, self.state.current_player)
        # sim_state.board.pieces = {k: v for k, v in self.state.board.pieces.items()}  # 深拷贝棋盘/
        new_sim_node = copy.deepcopy(sim_node)
        while sim_count < sim_count_max:
            end, winner = new_sim_node.state.is_end()
            if end:
                if winner != self.state.current_player:
                    return 1.0
                else:
                    return 0.0
            else:
                sim_count += 1
            re_count = 0
            re_count_quit = True
            while True:
                legal_moves = new_sim_node.state.get_legal_moves(new_sim_node.state.current_player)
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
            # if re_count_quit:
            #     if MCTSNode.loss_path(sim_node, move) == 'loss':
            #         return 'loss'
            #     else:
            #         sim_node.state.execute_move(move)
            # else:
            #     return None
            if re_count_quit:
                new_sim_node.state.execute_move(move)
            else:
                return None

    def loss_path_result(self, move):
        loss_path_result_node = self
        loss_path_result_node.state.execute_move(move)
        end, winner = loss_path_result_node.state.is_end()
        if end:
            if winner:
                return 1
        return 0

    def loss_path(self, move):
        loss_path_node = self
        loss_path_node.state.execute_move(move)
        result_add = 0
        legal_moves = []
        for legal_moves_f, legal_moves_t in\
                (loss_path_node.state.get_legal_moves(loss_path_node.state.current_player).items()):
            for legal_move_t in legal_moves_t:
                legal_moves.append((legal_moves_f, legal_move_t))
        for legal_move in legal_moves:
            result = MCTSNode.loss_path_result(loss_path_node, legal_move)
            result_add += result
        if result_add != 0:
            return 'loss'


# 定义蒙特卡洛树搜索类
class MCTS:
    def __init__(self, initial_state, iterations=1000):
        self.root = MCTSNode(initial_state)
        self.iterations = iterations

    def search(self):
        for _ in range(self.iterations):
            print('search迭代次数：', _)
            node = self.root
            if node.select_child() is not None:
                print('最佳子节点value:{};visits:{}.'.format(node.select_child().value, node.select_child().visits))

            # 选择阶段
            while node.is_fully_expanded() and (node.select_child() is not None):
                print('已遍历所有子节点，选择一个子节点')
                node = node.select_child()
            # 展开阶段
            if not node.is_fully_expanded():
                node = node.expand()
            # 模拟阶段
            result_value = 0
            i = 0
            for i in range(self.iterations//10):
                # print('开始第{}轮模拟'.format(i))
                result = node.simulate()
                if result is not None and result != 'loss':
                    result_value += result
                elif result == 'loss':
                    node.value = -100
                else:
                    break
            if i != 0:
                result_value = result_value / (i + 1)
            # 回溯阶段
            while node is not None:
                node.visits += 1
                node.value += result_value
                node = node.parent

    # 获取最佳动作
    def get_best_move(self):
        best_move = max(self.root.children.values(), key=lambda c: (c.value / c.visits))
        return list(self.root.children.keys())[list(self.root.children.values()).index(best_move)]


