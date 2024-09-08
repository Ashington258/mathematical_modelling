import random
from math import log
from scipy.stats import beta  # 用于贝叶斯更新的 Beta 分布


# 贝叶斯自适应马尔可夫决策中的Beta分布
class BetaDistribution:
    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta

    def sample(self):
        # 从当前分布中采样
        return random.betavariate(self.alpha, self.beta)

    def update(self, success):
        # 更新贝叶斯分布：成功则增加alpha，失败则增加beta
        self.alpha += success
        self.beta += 1 - success


# 使用贝叶斯更新的MDP状态
class BAMDPState:
    def __init__(
        self, decisions, parts, semi_products, final_product, n_c, prior_beliefs
    ):
        self.decisions = decisions
        self.parts = parts
        self.semi_products = semi_products
        self.final_product = final_product
        self.n_c = n_c
        self.prior_beliefs = prior_beliefs  # 不确定性信念

    def possible_moves(self):
        if len(self.decisions) < 16:  # 有16个决策
            return [0, 1]
        return []

    def move(self, decision):
        new_decisions = self.decisions[:]
        new_decisions.append(decision)
        # 产生新的状态
        return BAMDPState(
            new_decisions,
            self.parts,
            self.semi_products,
            self.final_product,
            self.n_c,
            self.prior_beliefs,
        )

    def is_terminal(self):
        return len(self.decisions) == 16

    def reward(self):
        # 用贝叶斯分布采样来更新我们对各零配件缺陷率的信念
        sampled_defect_rates = [
            self.prior_beliefs[i].sample() for i in range(len(self.parts))
        ]

        # 计算零配件购买成本
        C_c_p = sum(
            n_c * c_p
            for c_p, n_c in zip(
                [part["purchase_price"] for part in self.parts], self.n_c
            )
        )

        # 计算零配件检测成本
        C_c_d = sum(
            n_c * x * c_d
            for x, c_d, n_c in zip(
                self.decisions[:8],
                [part["inspection_cost"] for part in self.parts],
                self.n_c,
            )
        )

        # 成品次品率
        p_f = self.final_product["defect_rate"]

        # 使用采样的次品率计算检测合格后的零配件数量
        n_c_post_inspection = sum(
            n_c * (1 - x * p_c)
            for x, p_c, n_c in zip(self.decisions[:8], sampled_defect_rates, self.n_c)
        )

        # 成品数量
        n_f = n_c_post_inspection * (1 - p_f)

        # 计算其他相关成本
        C_d_f = self.final_product["inspection_cost"] * self.decisions[14] * n_f
        C_a_f = self.final_product["disassembly_cost"] * self.decisions[15] * n_f * p_f
        C_s = self.final_product["exchange_loss"] * self.decisions[14] * n_f * p_f
        C_s_f = self.final_product["assembly_cost"] * n_f

        # 计算利润
        S = self.final_product["market_price"] * n_f

        # 总成本
        Z = C_c_p + C_c_d + C_d_f + C_a_f + C_s + C_s_f - S

        return Z

    # 贝叶斯更新每次根据观测值调整参数
    def update_beliefs(self, observed_results):
        for i, success in enumerate(observed_results):
            self.prior_beliefs[i].update(success)


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


# 模拟函数返回模拟的结果及观测值
def simulate(state):
    observed_results = []

    # 生成观测结果，使其长度与零配件数量一致
    for i in range(len(state.parts)):
        observed_results.append(random.choice([0, 1]))  # 随机产生0或1表示观测到的结果

    while not state.is_terminal():
        possible_moves = state.possible_moves()
        move = random.choice(possible_moves)
        state = state.move(move)

    return state.reward(), observed_results


# MCTS算法的修改
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
            child_node = Node(new_state, node)
            node.children.append(child_node)
            node = child_node

        # 3. Simulation
        reward, observed_results = simulate(node.state)

        # 4. Backpropagation and Bayesian update
        while node is not None:
            node.update(reward)
            node.state.update_beliefs(observed_results)  # 更新贝叶斯信念
            node = node.parent


# 找到最优决策路径
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


parts = [
    {"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 4.0},  # 零配件 1
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 4.0},  # 零配件 2
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 4.0},  # 零配件 3
    {
        "defect_rate": 0.10,
        "purchase_price": 2,
        "inspection_cost": 0.0,
    },  # 零配件 4 (无检测成本)
    {
        "defect_rate": 0.10,
        "purchase_price": 8,
        "inspection_cost": 0.0,
    },  # 零配件 5 (无检测成本)
    {
        "defect_rate": 0.10,
        "purchase_price": 12,
        "inspection_cost": 0.0,
    },  # 零配件 6 (无检测成本)
    {
        "defect_rate": 0.10,
        "purchase_price": 8,
        "inspection_cost": 0.0,
    },  # 零配件 7 (无检测成本)
    {
        "defect_rate": 0.10,
        "purchase_price": 12,
        "inspection_cost": 0.0,
    },  # 零配件 8 (无检测成本)
]

semi_products = [
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    },  # 半成品 1
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    },  # 半成品 2
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    },  # 半成品 3
]

final_product = {
    "defect_rate": 0.10,
    "assembly_cost": 8.0,
    "inspection_cost": 6.0,
    "disassembly_cost": 10.0,
    "market_price": 200,
    "exchange_loss": 40.0,
}


n_c = [1 / 8] * 8  # 每种零配件数量均为相同比例

# 初始化贝叶斯先验信念
prior_beliefs = [BetaDistribution(2, 3) for _ in parts]  # 设置每个零件的初始信念

# 初始状态
initial_state = BAMDPState([], parts, semi_products, final_product, n_c, prior_beliefs)
root = Node(initial_state)

# 运行 MCTS
MCTS(root, iterations=10000)

# 找到最优决策路径
best_node = max(
    root.children, key=lambda x: x.value / x.visits if x.visits > 0 else float("-inf")
)

# 输出最优决策路径及其预期收益
full_decision_path = get_full_decision_path(best_node)
print(
    "最优决策路径:",
    full_decision_path,
    "预期收益:",
    -best_node.value / best_node.visits,
)
