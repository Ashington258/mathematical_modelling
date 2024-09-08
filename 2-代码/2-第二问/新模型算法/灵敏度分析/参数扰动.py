import os
import json
import numpy as np
import matplotlib.pyplot as plt

# 将工作目录更改为脚本所在目录
os.chdir(os.path.dirname(__file__))
print("Current working directory:", os.getcwd())


# 从JSON文件中读取数据
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 绘制敏感性分析曲线
def plot_sensitivity_analysis(param_name, param_values, profits):
    plt.figure(figsize=(10, 6))
    plt.plot(
        param_values, profits, marker="o", linestyle="-", color="b", label="Profit"
    )
    plt.title(f"Sensitivity Analysis of {param_name}", fontsize=16)
    plt.xlabel(f"{param_name}", fontsize=14)
    plt.ylabel("Profit", fontsize=14)
    plt.grid(True)
    plt.show()


# 从JSON文件中加载数据 (假设JSON文件名为'data.json')
data = load_data_from_json("data.json")

# 初始化变量
best_profit_overall = float("-inf")  # 初始化为负无穷大
best_decision_overall = None  # 初始化全局最优决策路径为空
all_scenarios = []  # 存储所有情况下的决策路径及收益

# 扰动参数设置
sensitivity_param = "part_1_defect_rate"  # 要进行灵敏度分析的参数
perturbation_range = np.linspace(0, 0.3, 10)  # 设置扰动范围 (0到0.3次品率的变化)

profits_sensitivity = []

# 遍历扰动范围，计算每个扰动下的收益
for perturbation in perturbation_range:
    total_profits = []  # 存储当前扰动下所有决策路径的收益
    # 修改要扰动的参数
    for case_data in data["scenarios"]:
        case_number = case_data["case"]
        p_c_1 = perturbation  # 对零件1的次品率进行扰动
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

        # 假设的零配件总数量
        n_c = 10  # 零配件总数量（假设值）

        # 遍历所有可能的决策组合 (2^4 = 16种)
        for x_1 in [0, 1]:  # 是否对零配件1进行检测
            for x_2 in [0, 1]:  # 是否对零配件2进行检测
                for y in [0, 1]:  # 是否对成品进行检测
                    for z in [0, 1]:  # 是否对不合格成品进行拆解
                        # 计算有效零配件的数量
                        effective_parts = n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)

                        # 成品数量计算
                        n_f = effective_parts * (1 - p_f)

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
                        profit = -Z  # 收益，目标函数的负值
                        total_profits.append(profit)

    # 记录当前扰动下的平均收益
    avg_profit = np.mean(total_profits)  # 对当前次品率下所有决策路径的收益取平均值
    profits_sensitivity.append(avg_profit)

# 绘制灵敏度分析图
plot_sensitivity_analysis(sensitivity_param, perturbation_range, profits_sensitivity)
