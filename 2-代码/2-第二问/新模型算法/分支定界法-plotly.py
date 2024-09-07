"""
Author: Ashington ashington258@proton.me
Date: 2024-09-07 23:39:52
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-07 23:39:58
FilePath: \2\分支定界法-plotly.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import json
import plotly.graph_objects as go


# 从JSON文件中读取数据
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

    # 使用Plotly进行可视化
    fig = go.Figure()

    colors = [
        "blue",
        "green",
        "red",
        "purple",
        "orange",
        "cyan",
    ]

    for idx, scenario in enumerate(all_scenarios):
        # 绘制折线图
        fig.add_trace(
            go.Scatter(
                x=decision_paths,
                y=scenario["profits"],
                mode="lines+markers",
                marker=dict(color=colors[idx]),
                name=f'Case {scenario["case"]}',
            )
        )
        # 重点标记最优决策路径点
        fig.add_trace(
            go.Scatter(
                x=[decision_paths[scenario["best_index"]]],
                y=[scenario["profits"][scenario["best_index"]]],
                mode="markers",
                marker=dict(
                    color=colors[idx], size=12, line=dict(color="black", width=2)
                ),
                name=f'Optimal Point Case {scenario["case"]}',
            )
        )

    # 图表设置
    fig.update_layout(
        title="Profit Analysis for Each Decision Path Across All Cases",
        xaxis_title="Decision Path",
        yaxis_title="Profit",
        xaxis=dict(tickangle=45),
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
    )

    fig.show()

    # 输出全局最优决策路径和对应的收益
    print(
        f"\n全局最优决策路径: (x_1={global_best_decision[0]}, x_2={global_best_decision[1]}, y={global_best_decision[2]}, z={global_best_decision[3]}) 在情况 {global_best_decision[4]} 中 -> 最终收益: {global_best_profit:.2f}"
    )


# 从JSON文件中加载数据 (假设JSON文件名为'data.json')
data = load_data_from_json("data.json")
branch_and_bound(data)
