import json
from itertools import product

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


# 选择特定情况
case_number = "5"  # 选择情况1
params = data["cases"][case_number]

# 穷举所有决策组合
decisions = [
    (d1, d2, d3, d4)
    for d1 in range(2)
    for d2 in range(2)
    for d3 in range(2)
    for d4 in range(2)
]
profits = [calculate_profit(d1, d2, d3, d4, params) for d1, d2, d3, d4 in decisions]

# 找出最高利润
max_profit = max(profits)
max_profit_index = profits.index(max_profit)
optimal_decision = decisions[max_profit_index]

# 输出结果
for decision, profit in zip(decisions, profits):
    print(f"Decision: {decision}, Profit: {profit:.2f}")

# 输出最优路径
print(f"/nOptimal Decision: {optimal_decision}, Maximum Profit: {max_profit:.2f}")
