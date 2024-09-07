import matplotlib.pyplot as plt


def calculate_cost_benefit(q1, c1, t1, q2, c2, t2, p, s, t_y, r, l, d):
    # 初始化结果列表
    results = []

    # 决策路径编号
    path_id = 0

    # 穷举所有决策组合
    for x1 in [True, False]:  # 是否检测零配件1
        for x2 in [True, False]:  # 是否检测零配件2
            for y in [True, False]:  # 是否检测成品
                for z in [True, False]:  # 是否拆解不合格成品
                    # 增加路径编号
                    path_id += 1

                    # 零配件成本
                    parts_cost = (c1 + t1 * x1) * (1 - q1 * x1) + (c2 + t2 * x2) * (
                        1 - q2 * x2
                    )

                    # 装配成本
                    assembly_cost = s

                    # 成品合格概率
                    good_parts_prob = (1 - q1 * x1) * (1 - q2 * x2)
                    good_product_prob = good_parts_prob * (1 - p)

                    # 成品检测成本
                    product_test_cost = t_y * y

                    # 销售收益
                    revenue = r * good_product_prob

                    # 不合格成品处理成本
                    defective_products = 1 - good_product_prob
                    if y:
                        defective_cost = (
                            product_test_cost + (d * z)
                        ) * defective_products
                    else:
                        defective_cost = (l + (d * z)) * defective_products

                    # 计算总成本
                    total_cost = (
                        parts_cost + assembly_cost + product_test_cost + defective_cost
                    )

                    # 存储结果
                    results.append(
                        {
                            "Path ID": path_id,
                            "Check Component 1": x1,
                            "Check Component 2": x2,
                            "Check Product": y,
                            "Dismantle Defective": z,
                            "Total Cost": total_cost,
                            "Revenue": revenue,
                            "Profit": revenue - total_cost,
                        }
                    )

    return results


# 情形参数
scenarios = [
    {
        "q1": 0.10,
        "c1": 4,
        "t1": 2,
        "q2": 0.10,
        "c2": 18,
        "t2": 3,
        "p": 0.10,
        "s": 6,
        "t_y": 3,
        "r": 56,
        "l": 6,
        "d": 5,
    },
    {
        "q1": 0.20,
        "c1": 4,
        "t1": 2,
        "q2": 0.20,
        "c2": 18,
        "t2": 3,
        "p": 0.20,
        "s": 6,
        "t_y": 3,
        "r": 56,
        "l": 6,
        "d": 5,
    },
    {
        "q1": 0.10,
        "c1": 4,
        "t1": 2,
        "q2": 0.10,
        "c2": 18,
        "t2": 3,
        "p": 0.10,
        "s": 6,
        "t_y": 3,
        "r": 56,
        "l": 30,
        "d": 5,
    },
    {
        "q1": 0.20,
        "c1": 4,
        "t1": 1,
        "q2": 0.20,
        "c2": 18,
        "t2": 1,
        "p": 0.20,
        "s": 6,
        "t_y": 2,
        "r": 56,
        "l": 30,
        "d": 5,
    },
    {
        "q1": 0.10,
        "c1": 4,
        "t1": 8,
        "q2": 0.20,
        "c2": 18,
        "t2": 1,
        "p": 0.10,
        "s": 6,
        "t_y": 2,
        "r": 56,
        "l": 10,
        "d": 5,
    },
    {
        "q1": 0.05,
        "c1": 4,
        "t1": 2,
        "q2": 0.05,
        "c2": 18,
        "t2": 3,
        "p": 0.05,
        "s": 6,
        "t_y": 3,
        "r": 56,
        "l": 10,
        "d": 40,
    },
]

# 对每种情形计算并找出最优路径
optimal_paths = []
for index, params in enumerate(scenarios):
    results = calculate_cost_benefit(**params)
    optimal_result = min(results, key=lambda x: x["Total Cost"])
    optimal_paths.append(optimal_result["Total Cost"])
    print(f"Scenario {index + 1} Optimal Path:")
    for key, value in optimal_result.items():
        print(f"  {key}: {value}")
    print()

# 可视化
plt.figure(figsize=(10, 5))
plt.plot(
    range(1, 7),
    optimal_paths,
    marker="o",
    linestyle="-",
    color="b",
    label="Optimal Path Total Cost",
)
plt.title("Optimal Path Total Cost Across Scenarios")
plt.xlabel("Scenario")
plt.ylabel("Total Cost")
plt.xticks(range(1, 7), [f"Scenario {i}" for i in range(1, 7)])
plt.grid(True)
plt.legend()
plt.show()
