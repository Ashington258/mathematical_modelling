import os
import json
import matplotlib.pyplot as plt
import numpy as np

# 将工作目录更改为脚本所在目录
os.chdir(os.path.dirname(__file__))
print("Current working directory:", os.getcwd())


# 从 JSON 文件中读取数据
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


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


def monte_carlo_sensitivity_analysis(data, n_simulations=1000):
    for case_data in data["scenarios"]:
        case_number = case_data["case"]
        p_c_1_samples = np.random.uniform(0, 0.1, n_simulations)
        profits = []
        for p_c_1 in p_c_1_samples:
            profit = calculate_profit(
                100,
                p_c_1,
                case_data["part_2_defect_rate"],
                case_data["part_1_purchase_price"],
                case_data["part_2_purchase_price"],
                case_data["part_1_detection_cost"],
                case_data["part_2_detection_cost"],
                case_data["product_defect_rate"],
                case_data["assembly_cost"],
                case_data["product_detection_cost"],
                case_data["market_price"],
                case_data["replacement_loss"],
                case_data["disassembly_cost"],
                0,
                0,
                0,
                0,  # 假定其他决策变量固定
            )
            profits.append(profit)

        # 绘制敏感度分析结果
        plt.figure()
        plt.scatter(p_c_1_samples, profits, alpha=0.5)
        plt.title(f"Profit Sensitivity to Part 1 Defect Rate in Case {case_number}")
        plt.xlabel("Part 1 Defect Rate (p_c_1)")
        plt.ylabel("Profit")
        plt.grid(True)
        plt.show()


# 加载数据
data_path = "./data.json"  # 设置你的数据文件路径
data = load_data_from_json(data_path)
monte_carlo_sensitivity_analysis(data)
