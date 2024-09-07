import random
from math import log  # 导入 log 函数


def MCTS(root, iterations):
    for _ in range(iterations):
        node = root
        # 1. Selection
        while node.is_fully_expanded() and not node.state.is_terminal():
            node = node.best_child()

        # 2. Expansion
        if not node.is_fully_expanded() and not node.state.is_terminal():
            possible_moves = node.state.possible_moves()
            move = random.choice(possible_moves)
            new_state = node.state.move(move)
            child_node = Node(new_state, node)  # 加入 parent 参数
            node.children.append(child_node)
            node = child_node

        # 3. Simulation
        reward = simulate(node.state)

        # 4. Backpropagation
        while node is not None:
            node.update(reward)
            node = node.parent


def simulate(state):
    # 这里需要定义一个模拟函数来评估从当前状态开始的随机玩法的结果
    while not state.is_terminal():
        possible_moves = state.possible_moves()
        move = random.choice(possible_moves)
        state = state.move(move)
    return state.reward()


# 在 Node 类中添加 parent 属性
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.value = 0
        self.visits = 0
        self.children = []

    def expand(self):
        for move in self.state.possible_moves():
            new_state = self.state.move(move)
            child_node = Node(new_state, self)
            self.children.append(child_node)

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.possible_moves())

    def best_child(self, c_param=1.4):
        # 使用 UCT 公式选择最佳子节点
        choices_weights = [
            (child.value / child.visits)
            + c_param * (2 * log(self.visits) / child.visits) ** 0.5
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def update(self, reward):
        self.visits += 1
        self.value += reward


class MDPState:
    def __init__(self, decisions, parts, semi_products, final_product, n_c):
        self.decisions = decisions
        self.parts = parts
        self.semi_products = semi_products
        self.final_product = final_product
        self.n_c = n_c

    def possible_moves(self):
        if len(self.decisions) < 16:  # 有 16 个决策
            return [0, 1]
        return []

    def move(self, decision):
        new_decisions = self.decisions[:]
        new_decisions.append(decision)
        return MDPState(
            new_decisions, self.parts, self.semi_products, self.final_product, self.n_c
        )

    def is_terminal(self):
        return len(self.decisions) == 16

    def reward(self):
        # 计算零配件购买成本 C^c_p
        C_c_p = sum(
            n_c * c_p
            for c_p, n_c in zip(
                [part["purchase_price"] for part in self.parts], self.n_c
            )
        )

        # 计算零配件检测成本 C^c_d
        C_c_d = sum(
            n_c * x * c_d
            for x, c_d, n_c in zip(
                self.decisions[:8],
                [part["inspection_cost"] for part in self.parts],
                self.n_c,
            )
        )

        # 成品次品率 p^f
        p_f = self.final_product["defect_rate"]

        # 检测合格后的零配件数量
        n_c_post_inspection = sum(
            n_c * (1 - x * p_c)
            for x, p_c, n_c in zip(
                self.decisions[:8],
                [part["defect_rate"] for part in self.parts],
                self.n_c,
            )
        )

        # 成品数量 n^f
        n_f = n_c_post_inspection * (1 - p_f)

        # 计算成品检测成本 C_d_f
        C_d_f = self.final_product["inspection_cost"] * self.decisions[14] * n_f

        # 计算成品拆解成本 C_a_f
        C_a_f = self.final_product["disassembly_cost"] * self.decisions[15] * n_f * p_f

        # 计算调换成本 C_s
        C_s = self.final_product["exchange_loss"] * self.decisions[14] * n_f * p_f

        # 计算成品装配成本 C_s_f
        C_s_f = self.final_product["assembly_cost"] * n_f

        # 计算利润 S
        S = self.final_product["market_price"] * n_f

        # 计算总成本 Z
        Z = C_c_p + C_c_d + C_d_f + C_a_f + C_s + C_s_f - S

        return -Z  # 返回负收益，因为我们是在最小化总成本


# 更新 parts, semi_products, final_product 和 n_c 的值
parts = [
    {"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 1},  # 零配件 1
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 1},  # 零配件 2
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 2},  # 零配件 3
    {"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 1},  # 零配件 4
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 1},  # 零配件 5
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 2},  # 零配件 6
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 1},  # 零配件 7
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 2},  # 零配件 8
]

semi_products = [
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "inspection_cost": 4,
        "disassembly_cost": 6,
    },  # 半成品 1
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "inspection_cost": 4,
        "disassembly_cost": 6,
    },  # 半成品 2
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "inspection_cost": 4,
        "disassembly_cost": 6,
    },  # 半成品 3
]

final_product = {
    "defect_rate": 0.10,
    "assembly_cost": 8,
    "inspection_cost": 6,
    "disassembly_cost": 10,
    "market_price": 200,
    "exchange_loss": 40,
}

# n_c = [100] * 8  # 每种零配件数量均为 100
n_c = [1] * 8  # 每种零配件数量均为 100
# 初始化状态
initial_state = MDPState([], parts, semi_products, final_product, n_c)
root = Node(initial_state)

# 运行 MCTS
MCTS(root, iterations=1000)

# 找到最优决策路径
best_node = max(
    root.children, key=lambda x: x.value / x.visits if x.visits > 0 else float("-inf")
)


# 构建完整决策路径
def get_decision_path(node):
    decisions = []
    while node.parent is not None:
        decisions.append(node.state.decisions[-1])  # 获取最新的决策
        node = node.parent
    return decisions[::-1]  # 反转顺序，得到从根节点到目标节点的决策顺序


def get_full_decision_path(node):
    decisions = []
    while node.parent is not None:
        decisions.append(node.state.decisions[-1])  # 获取最新的决策
        node = node.parent
    decisions.reverse()  # 反转顺序，得到从根节点到目标节点的决策顺序
    # 确保决策数组长度为16
    while len(decisions) < 16:
        decisions.append(0)  # 假设未指定的决策默认为0
    return decisions


# 使用新的函数获取完整决策路径
full_decision_path = get_full_decision_path(best_node)

print(
    "最优决策路径:",
    full_decision_path,
    "预期收益:",
    -best_node.value / best_node.visits,
)
