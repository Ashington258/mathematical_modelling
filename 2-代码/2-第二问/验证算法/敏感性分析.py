import json
import numpy as np
import matplotlib.pyplot as plt

# 从JSON文件读取数据
with open(
    "F:/1.Project/2.Ongoing_Projects/mathematical_modelling/2-代码/2-第二问/验证算法/data.json",
    "r",
) as file:
    data = json.load(file)


def calculate_profit(d1, d2, d3, d4, params):
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

    cost1 = price1 + (test_cost1 if d1 else 0)
    cost2 = price2 + (test_cost2 if d2 else 0)
    defect_cost1 = defect_rate1 * cost1
    defect_cost2 = defect_rate2 * cost2

    final_cost = (
        (1 - defect_rate1) * (1 - defect_rate2) * (cost1 + cost2 + assembly_cost)
    )
    if d3:
        final_cost += test_cost_final
    sale_income = (1 - defect_rate_final) * sale_price
    exchange_cost = defect_rate_final * exchange_loss

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


def simulate_profit(params, n_simulations=1000):
    defect_rates = np.random.uniform(0, 0.1, n_simulations)
    profits = []
    for defect_rate in defect_rates:
        params["part1_defective_rate"] = defect_rate
        profit = calculate_profit(
            0, 0, 0, 0, params
        )  # Assuming other decisions are fixed
        profits.append(profit)
    return defect_rates, profits


case_number = "5"
params = data["cases"][case_number]
defect_rates, profits = simulate_profit(params)

plt.scatter(defect_rates, profits, alpha=0.5)
plt.title("Profit Sensitivity to Part 1 Defective Rate")
plt.xlabel("Part 1 Defective Rate")
plt.ylabel("Profit")
plt.grid(True)
plt.show()
