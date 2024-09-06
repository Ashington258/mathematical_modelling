"""
Author: Ashington ashington258@proton.me
Date: 2024-09-06 15:38:16
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-06 15:48:22
FilePath: \mathematical_modelling\2-代码\2-第二问\2.py
Description: Optimization model for determining the cost-effectiveness of testing and disassembling electronic components during production.
联系方式:921488837@qq.com
Copyright (c) 2024 by Ashington, All Rights Reserved. 
"""

import numpy as np

# 定义参数
params = {
    "cost_part": [4, 18],  # 零配件的成本（两种零配件）
    "cost_assembly": 6,  # 装配成本
    "cost_reject": 56,  # 成品市场售价
    "cost_replacement": 6,  # 不合格成品的调换损失
    "cost_disassembly": 5,  # 拆解不合格成品的费用
    "defect_rate_part": [0.1, 0.1],  # 零配件的次品率
    "defect_rate_product": 0.1,  # 成品的次品率
    "test_cost_part": [2, 3],  # 零配件检测成本
    "test_cost_product": 3,  # 成品检测成本
}


# 成本计算函数
def calculate_cost(test_part, test_product, disassemble, reuse_parts):
    total_cost = 0
    part_costs = []
    reuse_savings = 0

    # 计算每种零配件的成本，考虑是否进行检测和重用
    for i in range(2):  # 对两种零配件进行操作
        if test_part[i]:
            defect_rate = 0  # 假设检测后次品被完全移除
        else:
            defect_rate = params["defect_rate_part"][i]

        part_cost = (
            params["cost_part"][i] * (1 - reuse_parts[i])
            + params["test_cost_part"][i] * test_part[i]
        )
        part_costs.append(part_cost)
        total_cost += part_cost

    # 计算成品的检测和次品处理成本
    if test_product:
        defect_rate_product = 0
    else:
        defect_rate_product = params["defect_rate_product"]

    total_cost += params["cost_assembly"]
    total_cost += params["test_cost_product"] * test_product

    if defect_rate_product > 0:
        if disassemble:
            total_cost += params["cost_disassembly"]
            reuse_savings = sum(part_costs)  # 假设拆解后所有零配件都能重用
        else:
            total_cost += params["cost_replacement"]

    return total_cost - reuse_savings


# 示例决策执行
decisions = {
    "test_part": [False, False],  # 零配件检测决策
    "test_product": True,  # 成品检测决策
    "disassemble": True,  # 是否拆解不合格成品
    "reuse_parts": [0.5, 0.5],  # 假设50%的零配件能被重用
}

cost = calculate_cost(
    decisions["test_part"],
    decisions["test_product"],
    decisions["disassemble"],
    decisions["reuse_parts"],
)
print(f"调整后的总成本: {cost}")
print(
    f"最佳策略: 检测零配件1: {decisions['test_part'][0]}, 检测零配件2: {decisions['test_part'][1]}, 检测成品: {decisions['test_product']}, 拆解不合格成品: {decisions['disassemble']}"
)
