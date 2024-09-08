"""
Author: Ashington ashington258@proton.me
Date: 2024-09-08 17:53:34
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 18:02:34
FilePath: \mathematical_modelling\2-代码\4-第四问\计算次品率\计算次品率.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import math
from scipy import stats


def calculate_defect_rate(defects, total_samples, confidence_level=0.95):
    """
    计算次品率和置信区间
    :param defects: 次品数量
    :param total_samples: 样本总数
    :param confidence_level: 置信水平 (默认 95%)
    :return: 次品率, 置信区间 (下限, 上限)
    """
    defect_rate = defects / total_samples
    standard_error = math.sqrt((defect_rate * (1 - defect_rate)) / total_samples)
    z_value = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    lower_bound = defect_rate - z_value * standard_error
    upper_bound = defect_rate + z_value * standard_error
    lower_bound = max(0, lower_bound)
    upper_bound = min(1, upper_bound)

    return defect_rate, (lower_bound, upper_bound)


def calculate_half_product_defect_rate(component_defect_rates):
    """
    根据多个零配件的次品率计算半成品的次品率
    假设零配件不合格则半成品不合格
    :param component_defect_rates: 零配件次品率的列表
    :return: 半成品次品率
    """
    combined_rate = 1
    for rate in component_defect_rates:
        combined_rate *= 1 - rate
    return 1 - combined_rate


def calculate_final_product_defect_rate(half_product_defect_rates):
    """
    根据多个半成品的次品率计算成品的次品率
    :param half_product_defect_rates: 半成品次品率的列表
    :return: 成品次品率
    """
    combined_rate = 1
    for rate in half_product_defect_rates:
        combined_rate *= 1 - rate
    return 1 - combined_rate


# 示例使用：
# 假设8个零配件的抽样检测数据如下：
defects_components = [10.0, 8.2, 5.5, 10.7, 7.7, 9.0, 6.6, 10.0]
total_samples_components = [100, 100, 100, 100, 100, 100, 100, 100]

# 计算8个零配件的次品率
component_defect_rates = []
for defects, total_samples in zip(defects_components, total_samples_components):
    defect_rate, _ = calculate_defect_rate(defects, total_samples)
    component_defect_rates.append(defect_rate)

print("零配件次品率：", [f"{rate*100:.2f}%" for rate in component_defect_rates])

# 假设半成品的组成如下（每个半成品由不同零配件组合而成）
# 半成品 1 由零配件 1, 2, 3 组成
# 半成品 2 由零配件 4, 5, 6 组成
# 半成品 3 由零配件 7, 8 组成
half_product_1_defect_rate = calculate_half_product_defect_rate(
    [component_defect_rates[0], component_defect_rates[1], component_defect_rates[2]]
)
half_product_2_defect_rate = calculate_half_product_defect_rate(
    [component_defect_rates[3], component_defect_rates[4], component_defect_rates[5]]
)
half_product_3_defect_rate = calculate_half_product_defect_rate(
    [component_defect_rates[6], component_defect_rates[7]]
)

print(f"半成品 1 的次品率: {half_product_1_defect_rate*100:.2f}%")
print(f"半成品 2 的次品率: {half_product_2_defect_rate*100:.2f}%")
print(f"半成品 3 的次品率: {half_product_3_defect_rate*100:.2f}%\n")

# 计算成品次品率 (由三个半成品装配成)
final_product_defect_rate = calculate_final_product_defect_rate(
    [half_product_1_defect_rate, half_product_2_defect_rate, half_product_3_defect_rate]
)

print(f"成品的次品率: {final_product_defect_rate*100:.2f}%")
