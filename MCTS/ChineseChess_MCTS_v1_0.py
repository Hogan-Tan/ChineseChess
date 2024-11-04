# 使用 MCTS 算法实现中国象棋的自动走棋

import copy
import math
import random
import time

from chessman.Shuai import Shuai


class GameState:

    def __init__(self, board, player):
        self.board = board
        self.player = player

    def is_end(self):
        red_shuai_exists = any(isinstance(piece, Shuai) and piece.is_red for piece in self.board.pieces.values())
        black_shuai_exists = any(isinstance(piece, Shuai) and not piece.is_red for piece in self.board.pieces.values())
        if red_shuai_exists and not black_shuai_exists:
            return True, True
        elif not red_shuai_exists and black_shuai_exists:
            return True, False
        else:
            return False, '游戏继续'

    def execute_move(self, move):  # move = ((x_f,y_f), (x_t,y_t))
        self.board.move(move[0][0], move[0][1], move[1][0] - move[0][0], move[1][1] - move[0][1])
        self.player = not self.player

    def get_legal_moves(self, player):
        legal_moves = {}
        for locate, piece in self.board.pieces.items():
            if piece.is_red == player:
                self.board.selected_piece = locate, piece
                (ox, oy) = locate
                get_moves = [x for x in self.board.get_move_locs(self.board, ox, oy) if x != locate]
                self.board.selected_piece = None
                legal_moves[locate] = get_moves
        return legal_moves  # legal_moves = {(x_f,y_f):[(x_t,y_t),...],...}


# 定义 MCTS 节点类
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = copy.deepcopy(state)
        self.parent = parent  # MCTSNode对象
        self.children = {}  # key为动作((x_f,y_f),(x_t,y_t))，值为子节点MCTSNode对象
        self.visits = 0
        self.value = 0.0

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        # 深拷贝 state
        result.state = copy.deepcopy(self.state, memo)
        result.state.board.pieces = {k: v for k, v in self.state.board.pieces.items()}

        # 深拷贝 parent
        if self.parent is not None:
            result.parent = copy.deepcopy(self.parent, memo)
        else:
            result.parent = None

        # 深拷贝 children
        result.children = {move: copy.deepcopy(child, memo) for move, child in self.children.items()}

        # 复制 visits 和 value
        result.visits = self.visits
        result.value = self.value
        return result

    def select_child(self, exploration_weight=math.sqrt(2)):  # 默认探索权重为2
        if not self.children:
            return None
        print('self.visits=', self.visits)
        selected_child = max(self.children.values(),
                             key=lambda child: child.value / (child.visits + 1) + exploration_weight * math.sqrt(
                                 (2 * math.log(self.visits))
                                 / (child.visits + 1)))
        return selected_child

    def expand(self):
        legal_moves = []
        expand_node_f = copy.deepcopy(self)
        for legal_moves_f, legal_moves_t in self.state.get_legal_moves(self.state.player).items():
            for legal_move_t in legal_moves_t:
                legal_moves.append((legal_moves_f, legal_move_t))  # legal_moves = [((x_f,y_f),(x_t,y_t)),...]
        if not legal_moves:
            return None
        unexpanded_moves = [move for move in legal_moves if move not in self.children]
        if not unexpanded_moves:
            return None
        move = random.choice(unexpanded_moves)
        expand_node = copy.deepcopy(self)
        expand_node.state.execute_move(move)
        child_node = MCTSNode(expand_node.state)
        expand_node_f.children[move] = child_node
        child_node.parent = expand_node_f
        return child_node

    def simulate(self):
        sim_count_max = 4  # 模拟的步数
        sim_count = 0
        sim_node = copy.deepcopy(self)
        while sim_count < sim_count_max:
            end, winner = sim_node.state.is_end()
            if end:
                if winner == self.state.player:
                    return 1.0
                else:
                    return 0.0
            else:
                sim_count += 1
            legal_moves = sim_node.state.get_legal_moves(sim_node.state.player)
            if not legal_moves:
                break
            moves = []
            for legal_moves_f, legal_moves_t in legal_moves.items():
                for legal_move_t in legal_moves_t:
                    moves.append((legal_moves_f, legal_move_t))
            move = random.choice(moves)
            sim_node.state.execute_move(move)
        del sim_node
        return 0.5


#  定义MCTS类
class MCTS:
    def __init__(self, state, iterations=1000):
        self.root = MCTSNode(state)
        self.iterations = iterations

    def search(self):
        search_start = time.time()
        player = self.root.state.player
        layer_m = 0
        for _ in range(self.iterations):
            legal_moves_count = sum(len(moves) for moves in
                                    self.root.state.get_legal_moves(self.root.state.player).values())
            layer = 0
            select_start = time.time()
            # 选择阶段；len(self.root.children) == legal_moves_count意味着所有子节点都已经扩展
            while self.root.children and len(self.root.children) == legal_moves_count:
                self.root = self.root.select_child()
                layer += 1
            if layer != layer_m:
                print('已完全展开第{}层'.format(layer))
                layer_m = layer
            select_end = time.time()
            print('单次选择用时：', select_end - select_start)

            # 扩展阶段
            if not len(self.root.children) == legal_moves_count:
                expand_start = time.time()
                child_node = self.root.expand()
                expand_end = time.time()
                print('单次扩展用时：', expand_end - expand_start)
                if child_node:
                    self.root = child_node
                else:
                    break
            else:
                break

            # 模拟阶段
            if self.root.state.player != player:
                self.root.state.player = not self.root.state.player
            result_cal = 0.0
            sim_start = time.time()
            for _ in range(self.iterations):  # 模拟次数
                result = self.root.simulate()
                result_cal += result
            result = result_cal / self.iterations
            sim_end = time.time()
            print('模拟{}次用时:{}'.format(self.iterations, sim_end - sim_start))

            # 反向传播阶段
            while self.root.parent:
                self.root.visits += 1
                self.root.value += result
                self.root = self.root.parent
            self.root.visits += 1

    def get_best_move(self):
        best_move = max(self.root.children.values(), key=lambda c: (c.value / c.visits))
        return list(self.root.children.keys())[list(self.root.children.values()).index(best_move)]
