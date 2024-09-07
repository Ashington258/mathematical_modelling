import os
import json
import matplotlib.pyplot as plt

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
    x_1,
    x_2,
    y,
    z,
):
    effective_parts = n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)  # 有效零配件数量
    n_f = effective_parts * (1 - p_f)  # 成品数量计算

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
    return -Z  # 收益，目标函数的负值


# 分支定界法求解
def branch_and_bound(data):
    global_best_profit = float("-inf")  # 初始化全局最优收益
    global_best_decision = None  # 初始化全局最优决策路径
    all_scenarios = []  # 存储所有情况下的决策路径及收益

    n_c = 1  # 零配件总数量（假设值，可以调整）

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

        initial_branch = (0, 0, 0, 0)
        stack = [(initial_branch, 0)]

        while stack:
            current_branch, depth = stack.pop()
            x_1, x_2, y, z = current_branch

            # 计算当前分支的收益
            profit = calculate_profit(
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
                x_1,
                x_2,
                y,
                z,
            )

            if depth == 4:
                profits.append(profit)

                if profit > best_profit:
                    best_profit = profit
                    best_decision = (x_1, x_2, y, z)

                if profit > global_best_profit:
                    global_best_profit = profit
                    global_best_decision = (x_1, x_2, y, z, case_number)

            else:
                next_depth = depth + 1
                for next_decision in [0, 1]:
                    new_branch = (
                        current_branch[:depth]
                        + (next_decision,)
                        + current_branch[depth + 1 :]
                    )
                    stack.append((new_branch, next_depth))

        print(
            f"最优决策路径: (x_1={best_decision[0]}, x_2={best_decision[1]}, y={best_decision[2]}, z={best_decision[3]}) 在情况 {case_number} 中 -> 最终收益: {best_profit:.2f}"
        )

        all_scenarios.append(
            {
                "case": case_number,
                "best_profit": best_profit,
            }
        )

    # 绘制柱状图
    cases = [f"Case {scenario['case']}" for scenario in all_scenarios]
    best_profits = [scenario["best_profit"] for scenario in all_scenarios]

    plt.figure(figsize=(10, 6))
    plt.bar(cases, best_profits, color="skyblue")
    plt.title("Best Profit for Each Case", fontsize=16)
    plt.xlabel("Case", fontsize=14)
    plt.ylabel("Best Profit", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    print(
        f"/n全局最优决策路径: (x_1={global_best_decision[0]}, x_2={global_best_decision[1]}, y={global_best_decision[2]}, z={global_best_decision[3]}) 在情况 {global_best_decision[4]} 中 -> 最终收益: {global_best_profit:.2f}"
    )


# 从JSON文件中加载数据 (假设JSON文件名为'data.json')
data = load_data_from_json("./data.json")
branch_and_bound(data)
