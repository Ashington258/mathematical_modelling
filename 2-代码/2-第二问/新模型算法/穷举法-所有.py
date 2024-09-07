import json
import matplotlib.pyplot as plt


# 从JSON文件中读取数据
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 初始化变量
best_profit_overall = float("-inf")  # 初始化为负无穷大
best_decision_overall = None  # 初始化全局最优决策路径为空
all_scenarios = []  # 存储所有情况下的决策路径及收益
decision_paths = []  # 存储所有的决策路径

# 从JSON文件中加载数据 (假设JSON文件名为'data.json')
data = load_data_from_json("data.json")

# 遍历所有6种情况
for case_data in data["scenarios"]:
    case_number = case_data["case"]
    profits = []  # 存储当前情况下所有决策的收益
    best_profit = float("-inf")  # 当前情况下的最优收益
    best_decision = None  # 当前情况下的最优决策

    # 读取参数
    p_c_1 = case_data["part_1_defect_rate"]
    p_c_2 = case_data["part_2_defect_rate"]
    c_p_1 = case_data["part_1_purchase_price"]
    c_p_2 = case_data["part_2_purchase_price"]
    c_d_1 = case_data["part_1_detection_cost"]
    c_d_2 = case_data["part_2_detection_cost"]
    p_f = case_data["product_defect_rate"]
    c_s_f = case_data["assembly_cost"]
    c_d_f = case_data["product_detection_cost"]
    s_f = case_data["market_price"]
    c_s = case_data["replacement_loss"]
    c_a_f = case_data["disassembly_cost"]

    # 假设的零配件总数量
    n_c = 10  # 零配件总数量（假设值，可以调整）

    # 遍历所有可能的决策组合 (2^4 = 16种)
    for x_1 in [0, 1]:  # 是否对零配件1进行检测
        for x_2 in [0, 1]:  # 是否对零配件2进行检测
            for y in [0, 1]:  # 是否对成品进行检测
                for z in [0, 1]:  # 是否对不合格成品进行拆解
                    # 决策路径
                    decision_path = f"({x_1}, {x_2}, {y}, {z})"
                    if case_number == 1:
                        decision_paths.append(decision_path)  # 仅需添加一次决策路径

                    # 计算有效零配件的数量
                    effective_parts = (
                        n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)
                    )  # 有效零配件数量

                    # 成品数量计算
                    n_f = effective_parts * (1 - p_f)

                    # 各项成本计算
                    C_c_p = n_c * (c_p_1 + c_p_2)  # 零配件购买成本
                    C_c_d = n_c * (x_1 * c_d_1 + x_2 * c_d_2)  # 零配件检测成本
                    C_d_f = c_d_f * y * n_f * (1 - p_f)  # 成品检测成本
                    C_a_f = c_a_f * z * n_f * p_f  # 成品拆解成本
                    C_s = c_s * y * n_f * p_f  # 调换成本
                    C_s_f = c_s_f * n_f  # 成品装配成本
                    S = s_f * n_f  # 利润

                    # 目标函数（总成本）
                    Z = C_c_p + C_c_d + C_d_f + C_a_f + C_s + C_s_f - S
                    profit = -Z  # 收益，目标函数的负值
                    profits.append(profit)

                    # 更新当前情况下的最优决策路径
                    if profit > best_profit:
                        best_profit = profit
                        best_decision = (x_1, x_2, y, z)

                    # 更新全局最优决策路径
                    if profit > best_profit_overall:
                        best_profit_overall = profit
                        best_decision_overall = (x_1, x_2, y, z, case_number)

    # 输出当前情况下的最优决策路径
    print(
        f"最优决策路径: (x_1={best_decision[0]}, x_2={best_decision[1]}, y={best_decision[2]}, z={best_decision[3]}) 在情况 {case_number} 中 -> 最终收益: {best_profit:.2f}"
    )

    # 将当前情况的收益存储到全局数据中
    all_scenarios.append(
        {
            "case": case_number,
            "profits": profits,
            "best_index": profits.index(best_profit),
        }
    )

# 使用SCI常用的颜色方案
colors = ["tab:blue", "tab:green", "tab:red", "tab:purple", "tab:orange", "tab:cyan"]
plt.figure(figsize=(12, 8))

for idx, scenario in enumerate(all_scenarios):
    # 绘制折线图
    plt.plot(
        decision_paths,
        scenario["profits"],
        color=colors[idx],
        marker="o",
        label=f'Case {scenario["case"]}',
    )
    # 重点标记最优决策路径点
    plt.scatter(
        scenario["best_index"],
        scenario["profits"][scenario["best_index"]],
        color=colors[idx],
        edgecolor="black",
        s=150,
        zorder=5,
        label=f"Optimal Point Case {scenario['case']}",
    )

# 图表设置
plt.title("Profit Analysis for Each Decision Path Across All Cases", fontsize=16)
plt.xlabel("Decision Path", fontsize=14)
plt.ylabel("Profit", fontsize=14)
plt.xticks(rotation=90, ha="right")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# 输出全局最优决策路径和对应的收益
print(
    f"\n全局最优决策路径: (x_1={best_decision_overall[0]}, x_2={best_decision_overall[1]}, y={best_decision_overall[2]}, z={best_decision_overall[3]}) 在情况 {best_decision_overall[4]} 中 -> 最终收益: {best_profit_overall:.2f}"
)
