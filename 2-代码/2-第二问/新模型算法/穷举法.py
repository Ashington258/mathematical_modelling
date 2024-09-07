import json


# 从JSON文件中读取数据
def load_data_from_json(file_path, case_number):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 查找对应的情况
    for scenario in data["scenarios"]:
        if scenario["case"] == case_number:
            return scenario

    return None


# 初始化变量
best_profit = float("-inf")  # 初始化为负无穷大
best_decision = None  # 初始化最优决策路径为空

# 从JSON文件中加载数据 (假设JSON文件名为'parameters.json')
case_number = 2  # 选择要读取的情况
data = load_data_from_json("data.json", case_number)

if data:
    # 读取参数
    p_c_1 = data["part_1_defect_rate"]
    p_c_2 = data["part_2_defect_rate"]
    c_p_1 = data["part_1_purchase_price"]
    c_p_2 = data["part_2_purchase_price"]
    c_d_1 = data["part_1_detection_cost"]
    c_d_2 = data["part_2_detection_cost"]
    p_f = data["product_defect_rate"]
    c_s_f = data["assembly_cost"]
    c_d_f = data["product_detection_cost"]
    s_f = data["market_price"]
    c_s = data["replacement_loss"]
    c_a_f = data["disassembly_cost"]

    # 假设的零配件总数量
    n_c = 1  # 零配件总数量（假设值，可以调整）

    # 遍历所有可能的决策组合 (2^4 = 16种)
    for x_1 in [0, 1]:  # 是否对零配件1进行检测
        for x_2 in [0, 1]:  # 是否对零配件2进行检测
            for y in [0, 1]:  # 是否对成品进行检测
                for z in [0, 1]:  # 是否对不合格成品进行拆解
                    # 计算有效零配件的数量
                    effective_parts = (
                        n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)
                    )  # 有效零配件数量

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

                    # 输出当前组合的决策路径和收益
                    print(
                        f"决策路径 (x_1={x_1}, x_2={x_2}, y={y}, z={z}) -> 收益: {profit:.2f}"
                    )

                    # 更新最优决策路径
                    if profit > best_profit:
                        best_profit = profit
                        best_decision = (x_1, x_2, y, z)

    # 输出最优决策路径和对应的收益
    print(
        f"\n最优决策路径: (x_1={best_decision[0]}, x_2={best_decision[1]}, y={best_decision[2]}, z={best_decision[3]}) -> 最终收益: {best_profit:.2f}"
    )
else:
    print(f"未找到对应的情况 {case_number}")
