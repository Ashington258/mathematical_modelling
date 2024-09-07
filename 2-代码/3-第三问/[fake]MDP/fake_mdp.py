import numpy as np
import pandas as pd

# 定义决策状态
states = [
    "零配件1",
    "零配件2",
    "零配件3",
    "零配件4",
    "零配件5",
    "零配件6",
    "零配件7",
    "零配件8",
    "半成品1",
    "半成品2",
    "半成品3",
    "成品",
]

# 定义行动：检测、不检测、拆解
actions = ["检测", "不检测", "拆解"]

# 定义修正后的次品率、成本等数据
component_defects = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
purchase_costs = [2, 8, 12, 2, 8, 12, 8, 12]
inspection_costs = [1, 1, 2, 1, 1, 2, 1, 2]
assembly_costs = [8, 8, 8]
inspection_costs_semi = [4, 4, 4]
disassembly_costs = [6, 6, 6]
market_price = 200
exchange_loss = 40

# 构建修正的奖励矩阵
rewards = np.array(
    [
        # 零配件
        [
            -purchase_costs[0] - inspection_costs[0],
            -purchase_costs[0],
            -disassembly_costs[0],
        ],  # 零配件1
        [
            -purchase_costs[1] - inspection_costs[1],
            -purchase_costs[1],
            -disassembly_costs[1],
        ],  # 零配件2
        [
            -purchase_costs[2] - inspection_costs[2],
            -purchase_costs[2],
            -disassembly_costs[2],
        ],  # 零配件3
        [
            -purchase_costs[3] - inspection_costs[3],
            -purchase_costs[3],
            -disassembly_costs[1],
        ],  # 零配件4
        [
            -purchase_costs[4] - inspection_costs[4],
            -purchase_costs[4],
            -disassembly_costs[1],
        ],  # 零配件5
        [
            -purchase_costs[5] - inspection_costs[5],
            -purchase_costs[5],
            -disassembly_costs[1],
        ],  # 零配件6
        [
            -purchase_costs[6] - inspection_costs[6],
            -purchase_costs[6],
            -disassembly_costs[2],
        ],  # 零配件7
        [
            -purchase_costs[7] - inspection_costs[7],
            -purchase_costs[7],
            -disassembly_costs[2],
        ],  # 零配件8
        # 半成品
        [
            -assembly_costs[0] - inspection_costs_semi[0],
            -assembly_costs[0],
            -disassembly_costs[0],
        ],  # 半成品1
        [
            -assembly_costs[1] - inspection_costs_semi[1],
            -assembly_costs[1],
            -disassembly_costs[1],
        ],  # 半成品2
        [
            -assembly_costs[2] - inspection_costs_semi[2],
            -assembly_costs[2],
            -disassembly_costs[2],
        ],  # 半成品3
        # 成品
        [
            market_price - inspection_costs_semi[2] - exchange_loss,
            market_price - exchange_loss,
            -disassembly_costs[2],
        ],  # 成品
    ]
)

# 构建修正后的转移概率矩阵，并规范化
transition_matrix = (
    np.ones((len(states), len(actions), len(states))) * 0.1
)  # 假设次品率固定影响概率
transition_matrix = transition_matrix / np.sum(
    transition_matrix, axis=2, keepdims=True
)  # 规范化转移概率

# 初始化价值函数和策略
values = np.zeros(len(states))
policy = np.zeros(len(states))

# 马尔可夫决策过程求解
gamma = 0.9  # 折扣因子
theta = 0.01  # 收敛阈值
converged = False

while not converged:
    delta = 0
    for state in range(len(states)):
        v = values[state]
        q_values = []
        # 计算每个行动的价值
        for action in range(len(actions)):
            q_value = rewards[state, action] + gamma * np.sum(
                transition_matrix[state, action] * values
            )
            q_values.append(q_value)
        values[state] = max(q_values)
        policy[state] = np.argmax(q_values)
        delta = max(delta, abs(v - values[state]))
    if delta < theta:
        converged = True

# 输出决策结果
results = pd.DataFrame(
    {
        "States": states,
        "Optimal Actions": [actions[int(policy[i])] for i in range(len(policy))],
        "Value Estimates": values,
    }
)

# 打印输出结果
print(results)
