import itertools

# 定义参数
# 情况1的参数
params = {
    "component_1_defective_rate": 0.10,
    "component_1_cost": 4,
    "component_1_test_cost": 2,
    "component_2_defective_rate": 0.10,
    "component_2_cost": 18,
    "component_2_test_cost": 3,
    "final_product_defective_rate": 0.10,
    "assembly_cost": 6,
    "final_product_test_cost": 3,
    "market_price": 56,
    "replacement_loss": 6,
    "disassembly_cost": 5,
}


# 决策路径遍历
def calculate_profit(decision, params):
    """
    计算给定决策路径的收益
    decision: 决策路径，长度为4的二进制列表
    params: 参数字典
    """
    # 提取参数
    c1_def_rate = params["component_1_defective_rate"]
    c1_cost = params["component_1_cost"]
    c1_test_cost = params["component_1_test_cost"]
    c2_def_rate = params["component_2_defective_rate"]
    c2_cost = params["component_2_cost"]
    c2_test_cost = params["component_2_test_cost"]
    final_def_rate = params["final_product_defective_rate"]
    assembly_cost = params["assembly_cost"]
    final_test_cost = params["final_product_test_cost"]
    market_price = params["market_price"]
    replacement_loss = params["replacement_loss"]
    disassembly_cost = params["disassembly_cost"]

    # 决策路径
    test_c1, test_c2, test_final, disassemble = decision

    # 计算零配件成本
    if test_c1:
        c1_final_cost = c1_cost + c1_test_cost * c1_def_rate
    else:
        c1_final_cost = c1_cost

    if test_c2:
        c2_final_cost = c2_cost + c2_test_cost * c2_def_rate
    else:
        c2_final_cost = c2_cost

    # 装配成本
    assembly_total_cost = c1_final_cost + c2_final_cost + assembly_cost

    # 计算成品的次品率
    effective_def_rate = 1 - (1 - c1_def_rate) * (1 - c2_def_rate)
    final_def_rate *= effective_def_rate

    if test_final:
        final_def_rate *= final_def_rate

    # 计算成品收益
    if disassemble:
        profit = (
            market_price
            - (final_def_rate * (replacement_loss + disassembly_cost))
            - assembly_total_cost
            - final_test_cost
        )
    else:
        profit = (
            market_price
            - (final_def_rate * replacement_loss)
            - assembly_total_cost
            - final_test_cost
        )

    return profit


# 遍历所有决策路径
def exhaustive_search(params):
    best_decision = None
    best_profit = float("-inf")

    for decision in itertools.product([0, 1], repeat=4):
        profit = calculate_profit(decision, params)
        print(f"Decision: {decision}, Profit: {profit}")
        if profit > best_profit:
            best_profit = profit
            best_decision = decision

    return best_decision, best_profit


# 运行穷举搜索
best_decision, best_profit = exhaustive_search(params)
print(f"Best Decision: {best_decision}, Best Profit: {best_profit}")
