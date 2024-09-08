import matplotlib.pyplot as plt

# 嵌入的JSON数据
data = {
    "scenarios": [
        {
            "case": 1,
            "part_1_defect_rate": 0.10,
            "part_1_purchase_price": 4,
            "part_1_detection_cost": 0,
            "part_2_defect_rate": 0.10,
            "part_2_purchase_price": 18,
            "part_2_detection_cost": 0,
            "product_defect_rate": 0.10,
            "assembly_cost": 6,
            "product_detection_cost": 0,
            "market_price": 56,
            "replacement_loss": 6,
            "disassembly_cost": 5,
        },
        {
            "case": 2,
            "part_1_defect_rate": 0.20,
            "part_1_purchase_price": 4,
            "part_1_detection_cost": 0,
            "part_2_defect_rate": 0.20,
            "part_2_purchase_price": 18,
            "part_2_detection_cost": 0,
            "product_defect_rate": 0.20,
            "assembly_cost": 6,
            "product_detection_cost": 0,
            "market_price": 56,
            "replacement_loss": 6,
            "disassembly_cost": 5,
        },
        {
            "case": 3,
            "part_1_defect_rate": 0.10,
            "part_1_purchase_price": 4,
            "part_1_detection_cost": 2,
            "part_2_defect_rate": 0.10,
            "part_2_purchase_price": 18,
            "part_2_detection_cost": 3,
            "product_defect_rate": 0.10,
            "assembly_cost": 6,
            "product_detection_cost": 3,
            "market_price": 56,
            "replacement_loss": 30,
            "disassembly_cost": 5,
        },
        {
            "case": 4,
            "part_1_defect_rate": 0.20,
            "part_1_purchase_price": 4,
            "part_1_detection_cost": 1,
            "part_2_defect_rate": 0.20,
            "part_2_purchase_price": 18,
            "part_2_detection_cost": 1,
            "product_defect_rate": 0.20,
            "assembly_cost": 6,
            "product_detection_cost": 2,
            "market_price": 56,
            "replacement_loss": 30,
            "disassembly_cost": 5,
        },
        {
            "case": 5,
            "part_1_defect_rate": 0.10,
            "part_1_purchase_price": 4,
            "part_1_detection_cost": 8,
            "part_2_defect_rate": 0.20,
            "part_2_purchase_price": 18,
            "part_2_detection_cost": 1,
            "product_defect_rate": 0.10,
            "assembly_cost": 6,
            "product_detection_cost": 2,
            "market_price": 56,
            "replacement_loss": 10,
            "disassembly_cost": 5,
        },
        {
            "case": 6,
            "part_1_defect_rate": 0.05,
            "part_1_purchase_price": 4,
            "part_1_detection_cost": 2,
            "part_2_defect_rate": 0.05,
            "part_2_purchase_price": 18,
            "part_2_detection_cost": 3,
            "product_defect_rate": 0.05,
            "assembly_cost": 6,
            "product_detection_cost": 3,
            "market_price": 56,
            "replacement_loss": 10,
            "disassembly_cost": 40,
        },
    ]
}


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
    effective_parts = n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)
    n_f = effective_parts * (1 - p_f)
    C_c_p = n_c * (c_p_1 + c_p_2)
    C_c_d = n_c * (x_1 * c_d_1 + x_2 * c_d_2)
    C_d_f = c_d_f * y * n_f * (1 - p_f)
    C_a_f = c_a_f * z * n_f * p_f
    C_s = c_s * y * n_f * p_f
    C_s_f = c_s_f * n_f
    S = s_f * n_f
    Z = C_c_p + C_c_d + C_d_f + C_a_f + C_s + C_s_f - S
    return -Z


def sensitivity_analysis(data):
    colors = ["b", "g", "r", "c", "m", "y"]
    plt.figure(figsize=(10, 6))

    for index, scenario in enumerate(data["scenarios"]):
        defect_rates = []
        profits = []
        initial_defect_rate = scenario["part_1_defect_rate"]
        while initial_defect_rate <= 1.0:
            defect_rates.append(initial_defect_rate)
            profit = calculate_profit(
                1,  # n_c
                initial_defect_rate,  # p_c_1
                scenario["part_2_defect_rate"],  # p_c_2
                scenario["part_1_purchase_price"],  # c_p_1
                scenario["part_2_purchase_price"],  # c_p_2
                scenario["part_1_detection_cost"],  # c_d_1
                scenario["part_2_detection_cost"],  # c_d_2
                scenario["product_defect_rate"],  # p_f
                scenario["assembly_cost"],  # c_s_f
                scenario["product_detection_cost"],  # c_d_f
                scenario["market_price"],  # s_f
                scenario["replacement_loss"],  # c_s
                scenario["disassembly_cost"],  # c_a_f
                0,
                0,
                1,
                0,  # x_1, x_2, y, z
            )
            profits.append(profit)
            initial_defect_rate += 0.05

        plt.plot(
            defect_rates, profits, label=f"Case {scenario['case']}", color=colors[index]
        )

    plt.title("Sensitivity Analysis of Part 1 Defect Rate on Profit")
    plt.xlabel("Part 1 Defect Rate")
    plt.ylabel("Profit")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


sensitivity_analysis(data)
