"""
Author: Ashington ashington258@proton.me
Date: 2024-09-08 14:33:20
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 14:33:20
FilePath: \mathematical_modelling\2-代码\1-第一问\样本大小对检测能力的影响.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import norm


# Function to calculate critical value based on sample size, defect rate, and confidence level
def calculate_critical_value(sample_size, p_nominal, confidence_level):
    z_score = norm.ppf(1 - (1 - confidence_level) / 2)
    critical_value = p_nominal + z_score * math.sqrt(
        (p_nominal * (1 - p_nominal)) / sample_size
    )
    return critical_value


# Range of sample sizes
sample_sizes = range(50, 1001, 50)  # From 50 to 1000 in steps of 50

# Parameters
p_nominal = 0.10  # Nominal defect rate of 10%
confidence_levels = [0.90, 0.95, 0.99]  # Various confidence levels

# Plotting
plt.figure(figsize=(10, 6))

for confidence_level in confidence_levels:
    critical_values = [
        calculate_critical_value(n, p_nominal, confidence_level) for n in sample_sizes
    ]
    plt.plot(
        sample_sizes, critical_values, label=f"Confidence {int(confidence_level*100)}%"
    )

plt.title("Critical Value vs Sample Size")
plt.xlabel("Sample Size")
plt.ylabel("Critical Value")
plt.legend()
plt.grid(True)
plt.show()
