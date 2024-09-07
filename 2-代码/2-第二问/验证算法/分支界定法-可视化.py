"""
Author: Ashington ashington258@proton.me
Date: 2024-09-07 15:18:53
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-07 15:18:53
FilePath: \mathematical_modelling\2-代码\2-第二问\验证算法\分支界定法-可视化.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import json
import matplotlib.pyplot as plt

# 从JSON文件读取数据
with open(
    "F:/1.Project/2.Ongoing_Projects/mathematical_modelling/2-代码/2-第二问/验证算法/data.json",
    "r",
) as file:
    data = json.load(file)


def calculate_profit(d1, d2, d3, d4, params):
    # 从参数字典读取值
    defect_rate1 = params["part1_defective_rate"]
    defect_rate2 = params["part2_defective_rate"]
    defect_rate_final = params["product_defective_rate"]
    price1 = params["part1_cost"]
    price2 = params["part2_cost"]
    assembly_cost = params["assembly_cost"]
    test_cost1 = params["part1_test_cost"]
    test_cost2 = params["part2_test_cost"]
    test_cost_final = params["product_test_cost"]
    sale_price = params["market_price"]
    exchange_loss = params["replacement_cost"]
    disassembly_cost = params["disassembly_cost"]

    # 零配件成本
    cost1 = price1 + (test_cost1 if d1 else 0)
    cost2 = price2 + (test_cost2 if d2 else 0)

    # 零配件检测
    if d1:
        defect_cost1 = defect_rate1 * price1
    else:
        defect_cost1 = defect_rate1 * cost1

    if d2:
        defect_cost2 = defect_rate2 * price2
    else:
        defect_cost2 = defect_rate2 * cost2

    # 装配成品成本
    final_cost = (
        (1 - defect_rate1) * (1 - defect_rate2) * (cost1 + cost2 + assembly_cost)
    )
    if d3:
        final_cost += test_cost_final
        sale_income = (1 - defect_rate_final) * sale_price
        exchange_cost = defect_rate_final * exchange_loss
    else:
        sale_income = sale_price
        exchange_cost = defect_rate_final * exchange_loss

    # 不合格成品处理
    if d4:
        disassembly_income = -disassembly_cost + (1 - defect_rate1) * (
            1 - defect_rate2
        ) * (cost1 + cost2 + assembly_cost - disassembly_cost)
    else:
        disassembly_income = -exchange_cost

    profit = (
        sale_income
        - final_cost
        - exchange_cost
        - disassembly_income
        - defect_cost1
        - defect_cost2
    )
    return profit


# 分支界定法求解
def branch_and_bound(params):
    best_profit = float("-inf")
    best_decision = None
    queue = [(0, 0, 0, 0, 0)]  # (d1, d2, d3, d4, level)

    while queue:
        d1, d2, d3, d4, level = queue.pop(0)

        # 计算当前节点的收益
        profit = calculate_profit(d1, d2, d3, d4, params)

        # 如果这是叶子节点，更新最佳决策
        if level == 4:
            if profit > best_profit:
                best_profit = profit
                best_decision = (d1, d2, d3, d4)
        else:
            # 生成子节点并加入队列，继续探索
            next_level = level + 1
            if next_level == 1:
                queue.append((1, d2, d3, d4, next_level))
                queue.append((0, d2, d3, d4, next_level))
            elif next_level == 2:
                queue.append((d1, 1, d3, d4, next_level))
                queue.append((d1, 0, d3, d4, next_level))
            elif next_level == 3:
                queue.append((d1, d2, 1, d4, next_level))
                queue.append((d1, d2, 0, d4, next_level))
            elif next_level == 4:
                queue.append((d1, d2, d3, 1, next_level))
                queue.append((d1, d2, d3, 0, next_level))

    return best_decision, best_profit


# 遍历所有6种情况
case_numbers = ["1", "2", "3", "4", "5", "6"]
profits = []

for case_number in case_numbers:
    params = data["cases"][case_number]
    optimal_decision, max_profit = branch_and_bound(params)
    profits.append(max_profit)
    print(
        f"Case {case_number}: Optimal Decision: {optimal_decision}, Maximum Profit: {max_profit:.2f}"
    )

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(case_numbers, profits, color="skyblue")
plt.xlabel("Case Number")
plt.ylabel("Maximum Profit")
plt.title("Maximum Profit for Each Case")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
