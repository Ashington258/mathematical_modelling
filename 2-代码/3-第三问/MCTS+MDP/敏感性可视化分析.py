import random
from math import log
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用黑体显示中文
plt.rcParams["axes.unicode_minus"] = False  # 正确显示负号

import networkx as nx


class Node:
    node_counter = 0  # 静态变量，给每个节点分配唯一ID

    def __init__(self, state, parent=None):
        self.id = Node.node_counter
        Node.node_counter += 1
        self.state = state
        self.parent = parent
        self.value = 0
        self.visits = 0
        self.children = []

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.possible_moves())

    def best_child(self, c_param=1.4):
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
        # 计算成本和利润的模拟函数
        return -random.randint(0, 100)  # 返回负值模拟成本


def MCTS(root, iterations, c_param=1.4):
    for _ in range(iterations):
        node = root
        # 1. Selection
        while node.is_fully_expanded() and not node.state.is_terminal():
            node = node.best_child(c_param=c_param)

        # 2. Expansion
        if not node.is_fully_expanded() and not node.state.is_terminal():
            possible_moves = node.state.possible_moves()
            move = random.choice(possible_moves)
            new_state = node.state.move(move)
            child_node = Node(new_state, node)
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


def get_best_reward(node):
    # 初始化最优奖励和对应节点
    best_reward = float("-inf")
    best_node = None

    # 使用递归函数来遍历所有节点
    def search_best(node):
        nonlocal best_reward, best_node
        if node.visits > 0:
            avg_reward = node.value / node.visits
            if avg_reward > best_reward:
                best_reward = avg_reward
                best_node = node
        for child in node.children:
            search_best(child)

    search_best(node)
    return best_reward


# 初始化状态
parts = [{"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 1}] * 8
semi_products = [
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "inspection_cost": 4,
        "disassembly_cost": 6,
    }
] * 3
final_product = {
    "defect_rate": 0.10,
    "assembly_cost": 8,
    "inspection_cost": 6,
    "disassembly_cost": 10,
    "market_price": 200,
    "exchange_loss": 40,
}
n_c = [1] * 8  # 每种零配件数量均为 100
initial_state = MDPState([], parts, semi_products, final_product, n_c)
root = Node(initial_state)

# 运行 MCTS
MCTS(root, iterations=1000)


def sensitivity_analysis(root, iterations=1000, c_values=[0.1, 0.5, 1.0, 1.4, 2.0]):
    results = []
    for c in c_values:
        MCTS(root, iterations, c_param=c)
        best_reward = get_best_reward(root)
        results.append((c, best_reward))

    c_vals, rewards = zip(*results)
    plt.figure()
    plt.plot(c_vals, rewards, marker="o")
    plt.xlabel("Exploration Parameter c")
    plt.ylabel("Best Reward")
    plt.title("Sensitivity Analysis on Exploration Parameter c")
    plt.grid(True)
    plt.show()


# 调用敏感性分析函数
sensitivity_analysis(root)
