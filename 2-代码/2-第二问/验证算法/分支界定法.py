import json

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


# 选择特定情况
case_number = "5"  # 选择情况6
params = data["cases"][case_number]

# 使用分支界定法寻找最优路径
optimal_decision, max_profit = branch_and_bound(params)

# 输出最优路径
print(f"\nOptimal Decision: {optimal_decision}, Maximum Profit: {max_profit:.2f}")
