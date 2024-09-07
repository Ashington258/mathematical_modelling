"""
Author: Ashington ashington258@proton.me
Date: 2024-09-07 23:41:48
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-07 23:41:54
FilePath: /mathematical_modelling/2-代码/2-第二问/新模型算法/分支定界法.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import os

# 将工作目录更改为脚本所在目录
os.chdir(os.path.dirname(__file__))
print("Current working directory:", os.getcwd())
import json
import matplotlib.pyplot as plt


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
    decision_paths = []  # 存储所有的决策路径

    # 假设的零配件总数量
    n_c = 1  # 零配件总数量（假设值，可以调整）

    # 遍历所有情况
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

        # 初始分支列表 (x_1, x_2, y, z)
        initial_branch = (0, 0, 0, 0)
        stack = [(initial_branch, 0)]  # 栈存储分支和层级（depth）

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

            if depth == 4:  # 已到达决策的最后一层
                profits.append(profit)
                decision_path = f"({x_1}, {x_2}, {y}, {z})"
                if case_number == 1:
                    decision_paths.append(decision_path)  # 仅需添加一次决策路径

                # 更新当前情况下的最优决策路径
                if profit > best_profit:
                    best_profit = profit
                    best_decision = (x_1, x_2, y, z)

                # 更新全局最优决策路径
                if profit > global_best_profit:
                    global_best_profit = profit
                    global_best_decision = (x_1, x_2, y, z, case_number)

            else:
                # 生成新的分支（扩展当前节点）
                next_depth = depth + 1
                for next_decision in [0, 1]:
                    new_branch = (
                        current_branch[:depth]
                        + (next_decision,)
                        + current_branch[depth + 1 :]
                    )
                    # 计算上界（可以用一个更好的估计方法）
                    # 简化示例中，假设不做其他调整，直接扩展
                    stack.append((new_branch, next_depth))

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
    colors = [
        "tab:blue",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:orange",
        "tab:cyan",
    ]
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
        f"/n全局最优决策路径: (x_1={global_best_decision[0]}, x_2={global_best_decision[1]}, y={global_best_decision[2]}, z={global_best_decision[3]}) 在情况 {global_best_decision[4]} 中 -> 最终收益: {global_best_profit:.2f}"
    )


# 从JSON文件中加载数据 (假设JSON文件名为'data.json')
data = load_data_from_json("./data.json")
branch_and_bound(data)
