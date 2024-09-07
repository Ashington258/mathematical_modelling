"""
Author: Ashington ashington258@proton.me
Date: 2024-09-07 14:32:32
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-07 14:40:16
FilePath: \mathematical_modelling\2-代码\2-第二问\穷举法.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import json


# 从JSON文件读取数据
def load_data_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


# 从指定情形中获取参数
def get_parameters(data, case_name):
    for case in data["cases"]:
        if case["name"] == case_name:
            return case
    raise ValueError(f"Case '{case_name}' not found in the data.")


# 计算成本函数
def calculate_cost(params):
    # 读取参数
    c_p = params["c_p"]
    c_d = params["c_d"]
    c_d_f = params["c_d_f"]
    c_a_f = params["c_a_f"]
    c_s = params["c_s"]
    p_c = params["p_c"]
    p_f = params["p_f"]
    s_f = params["s_f"]
    n_c = params["n_c"]

    # 初始化最优路径和最小成本
    best_path = None
    min_cost = float("inf")

    # 遍历所有可能的决策组合
    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    # 当前决策组合
                    x = [x1, x2]

                    # 计算成品数量
                    n_f = n_c * (1 - p_c[0] * x[0]) * (1 - p_c[1] * x[1])

                    # 成本函数
                    C_p_c = n_c * sum(c_p[i] for i in range(2))
                    C_d_c = n_c * sum(x[i] * c_d[i] for i in range(2))
                    C_d_f = c_d_f * y * n_f
                    C_a_f = c_a_f * p_f * z * n_f
                    C_s = c_s * p_f * y * n_f

                    # 利润函数
                    S = s_f * n_f

                    # 总成本目标函数
                    Z = C_p_c + C_d_c + (C_d_f + C_a_f + C_s - S)

                    # 输出当前决策组合及其总成本
                    print(f"决策路径: x1={x1}, x2={x2}, y={y}, z={z} => 总成本: {Z}")

                    # 更新最优路径和最小成本
                    if Z < min_cost:
                        min_cost = Z
                        best_path = (x1, x2, y, z)

    # 输出最优决策路径和最小成本
    print(
        f"最优决策路径: x1={best_path[0]}, x2={best_path[1]}, y={best_path[2]}, z={best_path[3]} => 最小总成本: {min_cost}"
    )


# 主函数
if __name__ == "__main__":
    # 从JSON文件中读取数据
    data = load_data_from_json(
        "F:/1.Project/2.Ongoing_Projects/mathematical_modelling/2-代码/2-第二问/data.json"
    )  # 替换为实际JSON文件路径

    # 用户选择使用的情形
    selected_case = "Case 6"  # 用户可以修改此处选择不同的情形

    # 获取选定情形的参数
    params = get_parameters(data, selected_case)

    # 计算成本
    calculate_cost(params)
