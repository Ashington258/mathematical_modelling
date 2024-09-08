import os
import json
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import matplotlib.cm as cm  # 导入 colormap

# 将工作目录更改为脚本所在目录
os.chdir(os.path.dirname(__file__))
print("Current working directory:", os.getcwd())


# 从 JSON 文件中读取数据
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 计算决策路径的收益
def calculate_profit(
    n_c,
    p_c_1,
    p_c_2,
    c_p_1,
    c_p_2,
    c_d_1,
    c_d_2,
    p_f,
    c_s_f,
    c_d_f,
    s_f,
    c_s,
    c_a_f,
    decision,
):
    x_1, x_2, y, z = decision
    effective_parts = n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)
    n_f = effective_parts * (1 - p_f)
    C_c_p = n_c * (c_p_1 + c_p_2)
    C_c_d = n_c * (x_1 * c_d_1 + x_2 * c_d_2)
    C_d_f = c_d_f * y * n_f * (1 - p_f)
    C_a_f = c_a_f * z * n_f * p_f
    C_s = c_s * y * n_f * p_f
    C_s_f = c_s_f * n_f
    S = s_f * n_f
    Z = C_c_p + C_c_d + C_d_f + C_a_f + C_s + C_s_f - S
    return -Z


# Monte Carlo sensitivity analysis for each decision path
def monte_carlo_sensitivity_on_decisions(
    case_data, n_simulations=100, ax=None, colors=None
):
    decisions = list(product([0, 1], repeat=4))  # Generate all decision combinations
    p_c_1_samples = np.random.uniform(0, 0.1, n_simulations)
    all_profits = []

    results = {}
    for decision, color in zip(decisions, colors):
        profits = []
        for p_c_1 in p_c_1_samples:
            profit = calculate_profit(
                100,
                p_c_1,
                case_data["part_2_defect_rate"],
                case_data["part_1_purchase_price"],
                case_data["part_2_purchase_price"],
                case_data["part_1_detection_cost"],
                case_data["part_2_detection_cost"],
                case_data["product_defect_rate"],
                case_data["assembly_cost"],
                case_data["product_detection_cost"],
                case_data["market_price"],
                case_data["replacement_loss"],
                case_data["disassembly_cost"],
                decision,
            )
            profits.append(profit)
        results[decision] = profits
        all_profits.extend(profits)

    max_profit = max(all_profits)

    for decision, profits in results.items():
        normalized_profits = [
            (profit / max_profit) * 100 for profit in profits
        ]  # Normalize
        ax.scatter(p_c_1_samples, normalized_profits, alpha=0.5, color=colors[decision])

    ax.set_title(f'Case {case_data["case"]}')
    ax.set_xlabel("Part 1 Defect Rate (p_c_1)")
    ax.set_ylabel("Normalized Profit (%)")
    ax.grid(True)


# Load data from JSON
data_path = "./data.json"
data = load_data_from_json(data_path)

# 创建6个子图
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
axs = axs.flatten()  # 将子图对象展平为一维数组

# 设置颜色映射，每个决策变量对应一种颜色
decisions = list(product([0, 1], repeat=4))  # 决策变量
colors = {
    decision: plt.cm.viridis(i / len(decisions)) for i, decision in enumerate(decisions)
}  # 使用 colormap 为决策变量分配颜色

# Perform sensitivity analysis on each case for all decision paths
for i, case_data in enumerate(data["scenarios"]):
    monte_carlo_sensitivity_on_decisions(case_data, 100, ax=axs[i], colors=colors)

# 添加统一的图例，并确保图例颜色与散点图中的一致
handles = [
    plt.Line2D(
        [],
        [],
        marker="o",
        color="w",
        markerfacecolor=colors[decision],
        markersize=10,
        label=f"Decision: {decision}",
    )
    for decision in decisions
]

fig.legend(handles=handles, loc="upper right", fontsize="small")

plt.tight_layout()
plt.show()
