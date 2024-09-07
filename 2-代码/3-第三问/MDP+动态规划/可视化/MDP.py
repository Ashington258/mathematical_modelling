"""
Author: Ashington ashington258@proton.me
Date: 2024-09-08 03:22:18
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 03:22:24
FilePath: \mathematical_modelling\2-代码\3-第三问\MDP+动态规划\可视化\MDP.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import numpy as np
from itertools import product
import matplotlib.pyplot as plt
import networkx as nx

# 定义问题中的常量
NUM_COMPONENTS = 8  # 简化组件数量用于测试
DISCOUNT_FACTOR = 0.9
MAX_ITERATIONS = 100
CONVERGENCE_THRESHOLD = 1e-4

# 定义组件及其相关成本和次品率（根据表2）
components = [
    {"defect_rate": 0.1, "purchase_cost": 2, "inspection_cost": 1},
    {"defect_rate": 0.1, "purchase_cost": 8, "inspection_cost": 1},
    {"defect_rate": 0.1, "purchase_cost": 12, "inspection_cost": 2},
    {"defect_rate": 0.1, "purchase_cost": 2, "inspection_cost": 1},
]

# 定义状态空间（0: 不检测，1: 检测）
states = list(product([0, 1], repeat=NUM_COMPONENTS))

# 定义动作空间（0: 不检测，1: 检测）
actions = list(product([0, 1], repeat=NUM_COMPONENTS))


# 定义奖励函数
def compute_reward(state, action):
    total_cost = sum(
        c["inspection_cost"] * a + c["purchase_cost"]
        for c, a in zip(components, action)
    )
    defect_probability = np.prod(
        [
            c["defect_rate"] if a == 0 else (c["defect_rate"] / 2)
            for c, a in zip(components, action)
        ]
    )
    sales_revenue = 200 * (1 - defect_probability)
    return sales_revenue - total_cost


# 使用向量化状态转移和奖励计算
def update_value_function(V, states, actions):
    new_V = np.zeros_like(V)
    for i, state in enumerate(states):
        rewards = np.array([compute_reward(state, action) for action in actions])
        values = rewards + DISCOUNT_FACTOR * V
        new_V[i] = np.max(values)
    return new_V


# 初始化值函数
V = np.zeros(len(states))

# 值迭代算法
for iteration in range(MAX_ITERATIONS):
    print(f"Iteration {iteration + 1} starting...")
    new_V = update_value_function(V, states, actions)
    delta = np.max(np.abs(V - new_V))
    V = new_V
    print(f"Iteration {iteration + 1} completed. Max delta: {delta:.6f}")
    if delta < CONVERGENCE_THRESHOLD:
        print(f"Converged after {iteration + 1} iterations.")
        break

# 打印结果
print("Optimal Values:")
for i, val in enumerate(V):
    print(f"State {states[i]}: Value = {val:.2f}")

# 构建状态转移图
G = nx.DiGraph()

# 添加节点和边
for i, state in enumerate(states):
    G.add_node(i, label=str(state), value=V[i])
    for action in actions:
        next_state = state  # 简化假设：状态保持不变
        G.add_edge(i, states.index(next_state), action=str(action))

# 可视化
pos = nx.spring_layout(G)
labels = nx.get_node_attributes(G, "label")
values = nx.get_node_attributes(G, "value")
edge_labels = nx.get_edge_attributes(G, "action")

plt.figure(figsize=(12, 8))
nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color="lightblue")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
plt.title("MDP State Transition and Optimal Policy Path")
plt.show()
