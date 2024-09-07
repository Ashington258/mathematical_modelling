'''
Author: Ashington ashington258@proton.me
Date: 2024-09-08 06:45:37
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 06:46:46
FilePath: \mathematical_modelling\2-代码\3-第三问\MCTS+MDP\逆穷举法可视化.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import plotly.express as px
class MDPState:
    def __init__(self, decisions, parts, semi_products, final_product, n_c):
        self.decisions = decisions
        self.parts = parts
        self.semi_products = semi_products
        self.final_product = final_product
        self.n_c = n_c

    def possible_moves(self):
        if len(self.decisions) < 16:  # 共有 16 个决策
            return [0, 1]  # 每个决策有两个选项，0 或 1
        return []

    def move(self, decision):
        new_decisions = self.decisions[:]
        new_decisions.append(decision)
        return MDPState(
            new_decisions, self.parts, self.semi_products, self.final_product, self.n_c
        )

    def is_terminal(self):
        return len(self.decisions) == 16  # 当决策长度达到 16 时，终止

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

n_c = [1] * 8  # 每种零配件数量均为 100


# 穷举法来验证最优路径
def exhaustive_search(state):
    if state.is_terminal():
        return state.reward(), state.decisions

    best_reward = float("-inf")
    best_decision_path = []

    # 穷举每一个可能的决策
    for move in state.possible_moves():
        next_state = state.move(move)
        reward, decision_path = exhaustive_search(next_state)

        if reward > best_reward:
            best_reward = reward
            best_decision_path = decision_path

    return best_reward, best_decision_path


# 初始状态
initial_state = MDPState([], parts, semi_products, final_product, n_c)

# 运行穷举法
best_reward, best_decision_path = exhaustive_search(initial_state)

print("穷举法找到的最优决策路径:", best_decision_path)
print("穷举法找到的最优收益:", best_reward)


# 收集所有决策路径和奖励
def exhaustive_search(state, path_rewards, current_path=[]):
    if state.is_terminal():
        reward = state.reward()
        path_rewards.append((current_path + [state.reward()], reward))
        return reward, current_path

    best_reward = float("-inf")
    best_decision_path = []

    # 穷举每一个可能的决策
    for move in state.possible_moves():
        next_state = state.move(move)
        reward, decision_path = exhaustive_search(
            next_state, path_rewards, current_path + [move]
        )

        if reward > best_reward:
            best_reward = reward
            best_decision_path = decision_path

    return best_reward, best_decision_path


# 初始化状态
initial_state = MDPState([], parts, semi_products, final_product, n_c)
path_rewards = []

# 运行穷举法
best_reward, best_decision_path = exhaustive_search(initial_state, path_rewards)

# 准备数据用于 Plotly
paths = ["".join(map(str, pr[0])) for pr in path_rewards]  # 将决策列表转换为字符串
rewards = [pr[1] for pr in path_rewards]

# 使用 Plotly 创建交互式散点图
fig = px.scatter(
    x=paths,
    y=rewards,
    labels={"x": "Decision Path", "y": "Reward"},
    title="Decision Paths and Their Rewards",
)
fig.show()

print("穷举法找到的最优决策路径:", best_decision_path)
print("穷举法找到的最优收益:", best_reward)
