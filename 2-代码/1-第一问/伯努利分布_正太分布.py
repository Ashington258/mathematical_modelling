'''
Author: Ashington ashington258@proton.me
Date: 2024-09-08 14:20:18
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 14:20:24
FilePath: \mathematical_modelling\2-代码\1-第一问\伯努利分布_正太分布.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import math
from scipy.stats import norm


# 计算样本量的函数
def calculate_sample_size(p_hat, error_margin, confidence_level):
    # 获取正态分布临界值 z_score
    z_score = norm.ppf(1 - (1 - confidence_level) / 2)

    # 计算样本量
    n = (z_score**2 * p_hat * (1 - p_hat)) / (error_margin**2)

    return math.ceil(n)


# 样本检测的函数
def check_acceptance_rejection(
    sample_size, observed_defect_rate, p_nominal, confidence_level, accept=True
):
    z_score = norm.ppf(1 - (1 - confidence_level) / 2)
    # 计算临界值
    critical_value = p_nominal + z_score * math.sqrt(
        (p_nominal * (1 - p_nominal)) / sample_size
    )

    if accept:
        return observed_defect_rate <= critical_value
    else:
        return observed_defect_rate > critical_value


# 参数设定
p_nominal = 0.10  # 标称次品率10%
confidence_95 = 0.95  # 95% 信度
confidence_90 = 0.90  # 90% 信度
error_margin = 0.05  # 误差容忍度

# 计算拒收方案 (95% 信度)
sample_size_95 = calculate_sample_size(p_nominal, error_margin, confidence_95)
print(f"在95%的信度下拒收零配件所需的样本量: {sample_size_95}")

# 计算接收方案 (90% 信度)
sample_size_90 = calculate_sample_size(p_nominal, error_margin, confidence_90)
print(f"在90%的信度下接收零配件所需的样本量: {sample_size_90}")

# 假设我们从样本中得到了一个实际的次品率
observed_defect_rate = 0.12  # 实际观察到的次品率12%

# 检查是否拒收 (95% 信度)
is_reject_95 = check_acceptance_rejection(
    sample_size_95, observed_defect_rate, p_nominal, confidence_95, accept=False
)
print(f"在95%的信度下，是否拒收零配件: {'是' if is_reject_95 else '否'}")

# 检查是否接收 (90% 信度)
is_accept_90 = check_acceptance_rejection(
    sample_size_90, observed_defect_rate, p_nominal, confidence_90, accept=True
)
print(f"在90%的信度下，是否接收零配件: {'是' if is_accept_90 else '否'}")
