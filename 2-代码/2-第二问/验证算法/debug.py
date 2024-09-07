"""
Author: Ashington ashington258@proton.me
Date: 2024-09-07 14:06:57
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-07 14:07:04
FilePath: \mathematical_modelling\2-代码\2-第二问\debug.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

# 参数
c_p = [4, 18]  # 零配件购买成本
c_d = [2, 3]  # 零配件检测成本
c_d_f = 3  # 成品检测成本
c_a_f = 5  # 成品拆解成本
c_s = 6  # 调换成本
p_c = [0.1, 0.1]  # 零配件次品率
p_f = 0.1  # 成品次品率
s_f = 56  # 成品售价
n_c = 1  # 零配件数量

# 决策变量 (是否检测或者拆解)
x = [0, 0]  # 是否检测零配件1, 2
y = 0  # 是否检测成品
z = 0  # 是否拆解成品

# 成品数量
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

# 输出总成本
print(f"总成本目标函数值: {Z}")
